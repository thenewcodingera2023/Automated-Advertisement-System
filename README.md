Automated Advertisement Generation System
An advanced platform for automating high-quality audio and video advertisement production using state-of-the-art AI, with seamless integrations for data management and media storage.

🚀 Overview

The Automated Advertisement Generation System revolutionizes ad production by automating the creation of professional audio and video content. Powered by cutting-edge AI for text-to-speech and speech recognition, it integrates with Airtable for data management and Google Drive for media storage, offering an efficient, scalable solution.
This project demonstrates a powerful combination of performance-optimized C++ and flexible Python, showcasing technical versatility and real-world problem-solving with modern tools.

✨ Features

High-Quality Audio Generation: Natural-sounding speech from text using Tacotron 2 and WaveGlow (LibTorch in C++, PyTorch in Python).

Accurate Speech Transcription: Precise audio-to-text conversion with Whisper for automated subtitles (ONNX Runtime in C++, Transformers in Python).

Seamless Media Integration: Combines audio and video with FFmpeg (C++) or MoviePy (Python) for polished ad videos.

Efficient Data Management: Real-time project data handling via Airtable API.

Scalable Storage: Uploads media to Google Drive for reliable storage.

Asynchronous Processing: Scalable task queuing with Redis (C++) and Celery (Python).

API-Driven Workflow: Webhook endpoints for integration with external systems like Airtable.


🏗️ Architecture

The system features a modular, dual-component design for performance and flexibility:

C++ Service: Optimized for speed using Crow (web server), Redis (task queuing), and AI inference with LibTorch (Tacotron 2, WaveGlow) and ONNX Runtime (Whisper). Ideal for resource-constrained environments.

Python Service: Built for rapid development with Flask (web server), Celery (task queuing), and Python libraries like Transformers and MoviePy. Perfect for customization and Python ecosystems.


Both services expose a /webhook endpoint, queue tasks via Redis/Celery, process them with AI and media tools, and update results in Airtable while uploading outputs to Google Drive.

🛠️ Technologies

Programming Languages

C++: Performance-critical components.

Python: Flexible, rapid development.


Web Frameworks

Crow (C++): Lightweight HTTP server.

Flask (Python): Simple, extensible web framework.


Task Queuing

Redis (C++): High-speed task queuing.

Celery (Python): Distributed task queue with Redis broker.


AI Models & Libraries

Tacotron 2 & WaveGlow: Text-to-speech (LibTorch in C++, PyTorch in Python).

Whisper: Speech recognition (ONNX Runtime in C++, Transformers in Python).


Media Processing

FFmpeg (C++): Audio and video merging.

MoviePy (Python): Video editing and subtitle integration.


Integrations

Airtable API: Data management.

Google Drive API: Media storage.


Additional Libraries

C++: libcurl, Boost.Asio, spdlog (HTTP, async, logging).

Python: OpenCV, Tenacity (video processing, retries).


📦 Installation & Setup

Prerequisites

Redis: Install and run Redis server.

Airtable: Get API key, base ID, and table name.

Google Drive: Set up API credentials with folder access.


C++ Service

Install Dependencies: Crow, Redis++, libcurl, JsonCpp, LibTorch, ONNX Runtime, spdlog, Boost (use apt, brew, or compile from source).

Compile: Use g++ with appropriate include/library paths.

Run: Execute the compiled binary.


Python Service

Install Dependencies:
pip install flask celery redis airtable-python-wrapper google-api-python-client torch transformers moviepy opencv-python tenacity


Configure Celery: Ensure Redis is running (redis://localhost:6379/0).

Run:
python automated.py



🎮 Usage

Trigger the system via the /webhook endpoint with POST requests.
Webhook Payload
{
  "action": "generateAudioVideo",
  "recordId": "rec1234567890"
}

Supported Actions

generateAudioVideo: Generates audio from Airtable text and uploads to Google Drive.

mergeAudioVideo: Merges audio/video, adds subtitles via transcription, and uploads.


Workflow

Send POST request to /webhook with action and record ID.

Task is queued and processed asynchronously.

Check progress/results in Airtable.


🌟 Examples

Audio Generation:

Send: {"action": "generateAudioVideo", "recordId": "rec123"}
Output: Audio generated with Tacotron 2/WaveGlow, uploaded to Google Drive, Airtable updated.


Video with Subtitles:

Send: {"action": "mergeAudioVideo", "recordId": "rec123"}
Output: Audio/video merged, subtitles added via Whisper, uploaded, Airtable updated.



🤝 Contributing

We welcome contributions! To get started:

Fork the repository.

Create a feature branch: git checkout -b feature-name.

Commit changes: git commit -m "Add feature".

Submit a pull request.


📜 License

This project is licensed under the MIT License.

🙌 Acknowledgments

AI Models: Tacotron 2, WaveGlow (NVIDIA), Whisper (OpenAI).

Tools: FFmpeg, MoviePy, Airtable, Google Drive API.

Libraries: Crow, Flask, Celery, Redis, LibTorch, ONNX Runtime, Transformers.
