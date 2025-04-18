# Imports
from flask import Flask, request, jsonify
from celery import Celery
from airtable import Airtable
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import torch
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
from transformers import pipeline
import logging
import cv2
from tenacity import retry, wait_exponential, stop_after_attempt

# Configurations
AIRTABLE_API_KEY = 'your_airtable_api_key'
AIRTABLE_BASE_ID = 'your_base_id'
AIRTABLE_TABLE_NAME = 'your_table_name'
GOOGLE_DRIVE_FOLDER_ID = 'your_google_drive_folder_id'
SCOPES = ['https://www.googleapis.com/auth/drive']

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask and Celery setup
app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Load AI models
tacotron2 = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_tacotron2', pretrained=True).eval()
waveglow = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_waveglow', pretrained=True).eval()
if torch.cuda.is_available():
    tacotron2, waveglow = tacotron2.cuda(), waveglow.cuda()
transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-base")

# Clients
airtable_client = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, api_key=AIRTABLE_API_KEY)
creds, _ = google.auth.default(scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

# Helper Functions
def generate_speech(text, beam_width=5):
    """Generate audio with beam search."""
    with torch.no_grad():
        sequence = np.array(tacotron2.text_to_sequence(text, ['english_cleaners']))[None, :]
        sequence = torch.from_numpy(sequence).long().cuda() if torch.cuda.is_available() else sequence
        mel_outputs, _, _ = tacotron2.infer(sequence, beam_width=beam_width)
        audio = waveglow.infer(mel_outputs).cpu().numpy()[0] * 32767
        return audio.astype(np.int16).tobytes()

def transcribe_audio(audio_path, confidence_threshold=0.85):
    """Transcribe audio with confidence filtering."""
    result = transcriber(audio_path, return_timestamps=True)
    return [chunk for chunk in result['chunks'] if chunk.get('confidence', 1.0) >= confidence_threshold]

def interpolate_frames(video_clip, factor=2):
    """Interpolate frames using optical flow."""
    frames = [frame for frame in video_clip.iter_frames()]
    flow = cv2.optflow.createOptFlow_DeepFlow()
    interpolated = []
    for i in range(len(frames) - 1):
        frame1, frame2 = frames[i], frames[i + 1]
        flow_field = flow.calc(frame1, frame2, None)
        for j in range(1, factor):
            alpha = j / factor
            interpolated.append(cv2.addWeighted(frame1, 1 - alpha, frame2, alpha, 0))
        interpolated.append(frame2)
    return VideoFileClip.from_frames(interpolated, fps=video_clip.fps * factor)

def add_subtitles_to_video(video_clip, subtitles_data):
    """Add subtitles to video."""
    generator = lambda txt: TextClip(txt, font='Arial', fontsize=24, color='white', bg_color='black')
    subtitles = [(chunk['timestamp'][0], chunk['timestamp'][1], chunk['text']) for chunk in subtitles_data]
    return CompositeVideoClip([video_clip, SubtitlesClip(subtitles, generator).set_pos(('center', 'bottom'))])

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(5))
def upload_to_drive(file_path, folder_id):
    """Upload file to Google Drive with retries."""
    file_metadata = {'name': os.path.basename(file_path), 'parents': [folder_id]}
    media = MediaFileUpload(file_path, mimetype='video/mp4' if file_path.endswith('.mp4') else 'audio/wav')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    drive_service.permissions().create(fileId=file.get('id'), body={'type': 'anyone', 'role': 'reader'}).execute()
    return drive_service.files().get(fileId=file.get('id'), fields='webContentLink').execute().get('webContentLink')

# Webhook Endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle Airtable webhook requests."""
    data = request.json
    action, record_id = data.get('action'), data.get('recordId')
    if not action or not record_id:
        return jsonify({'error': 'Missing action or recordId'}), 400
    if action == 'generateAudioVideo':
        generate_audio_video.apply_async(args=[record_id], priority=1)
    elif action == 'mergeAudioVideo':
        merge_audio_video.apply_async(args=[record_id], priority=2)
    else:
        return jsonify({'error': 'Invalid action'}), 400
    return jsonify({'status': 'Task queued'}), 202

# Celery Tasks
@celery.task
def generate_audio_video(record_id):
    """Generate and upload audio."""
    record = airtable_client.get(record_id)
    text, name = record['fields'].get('Text Prompt'), record['fields'].get('Goods name')
    if not text or not name:
        raise ValueError("Missing Text Prompt or Goods name")
    audio_data = generate_speech(text)
    audio_path = f"{name}.wav"
    with open(audio_path, 'wb') as f:
        f.write(audio_data)
    link = upload_to_drive(audio_path, GOOGLE_DRIVE_FOLDER_ID)
    airtable_client.update(record_id, {'Audio ': [{'url': link, 'filename': audio_path}], 'Audio Complete': True})

@celery.task
def merge_audio_video(record_id):
    """Merge audio/video, add subtitles, and upload."""
    record = airtable_client.get(record_id)
    name = record['fields'].get('Goods name')
    audio_url = record['fields'].get('Audio ', [{}])[0].get('url')
    video_url = record['fields'].get('Video', [{}])[0].get('url')
    if not name or not audio_url or not video_url:
        raise ValueError("Missing required fields")
    audio_path = f"{name}_audio.wav"
    video_path = f"{name}_video.mp4"
    os.system(f"curl -L {audio_url} -o {audio_path}")
    os.system(f"curl -L {video_url} -o {video_path}")
    subtitles = transcribe_audio(audio_path)
    video = VideoFileClip(video_path).set_audio(AudioFileClip(audio_path))
    smooth_video = interpolate_frames(video)
    final_video = add_subtitles_to_video(smooth_video, subtitles)
    final_path = f"{name}_final.mp4"
    final_video.write_videofile(final_path, codec='libx264', audio_codec='aac')
    link = upload_to_drive(final_path, GOOGLE_DRIVE_FOLDER_ID)
    airtable_client.update(record_id, {'Audio + Video ': [{'url': link, 'filename': final_path}], 'Merge Complete ': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)