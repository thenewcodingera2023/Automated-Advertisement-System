Automated Advertisement Generation System

Overview
The Automated Advertisement Generation System is an advanced platform designed to revolutionize advertisement production by automating the creation of high-quality audio and video content. Leveraging state-of-the-art AI technologies for text-to-speech and speech recognition, this system integrates seamlessly with Airtable for data management and Google Drive for media storage, delivering an efficient and scalable solution for generating professional advertisements.
This project showcases a sophisticated blend of performance-optimized C++ and flexible Python implementations, demonstrating technical versatility and the ability to tackle complex, real-world challenges with cutting-edge tools.
Features

High-Quality Audio Generation: Produces natural-sounding speech from text using Tacotron 2 and WaveGlow, powered by LibTorch (C++) and PyTorch (Python).
Accurate Speech Transcription: Employs Whisper for precise audio-to-text conversion, enabling automated subtitle generation (ONNX Runtime in C++, Transformers in Python).
Seamless Media Integration: Combines audio and video streams with FFmpeg (C++) or MoviePy (Python) to create polished advertisement videos.
Efficient Data Management: Integrates with Airtable to fetch, update, and manage project data in real time.
Scalable Storage Solution: Uploads generated media files to Google Drive for reliable, accessible storage.
Asynchronous Task Processing: Utilizes Redis (C++) and Celery (Python) for efficient, scalable task queuing and execution.
API-Driven Workflow: Exposes webhook endpoints for seamless integration with external systems, such as Airtable webhooks.

Architecture
The system is engineered with a modular, dual-component architecture to balance performance and flexibility:

C++ Service: Optimized for speed and efficiency, this service leverages Crow as a lightweight web server, Redis for task queuing, and high-performance AI inference with LibTorch (Tacotron 2, WaveGlow) and ONNX Runtime (Whisper). It is ideal for deployment in resource-constrained or performance-critical environments.

Python Service: Built for ease of development and rapid prototyping, this service uses Flask as the web server, Celery for task queuing, and integrates Python libraries like Transformers and MoviePy for AI-driven media processing. It excels in environments requiring extensive customization and integration with Python ecosystems.


Both services expose a /webhook endpoint to receive requests, queue tasks asynchronously via Redis or Celery, process them using AI and media tools, and update results in Airtable while uploading outputs to Google Drive.
Technologies Used
Programming Languages

C++: For performance-critical components.
Python: For flexible, rapid development.

Web Frameworks

Crow (C++): Lightweight HTTP server.
Flask (Python): Simple and extensible web framework.

Task Queuing

Redis (C++): High-speed task queuing and messaging.
Celery (Python): Distributed task queue with Redis broker.

AI Models and Libraries

Tacotron 2 and WaveGlow: Text-to-speech generation (LibTorch in C++, PyTorch in Python).
Whisper: Speech recognition (ONNX Runtime in C++, Transformers in Python).

Media Processing

FFmpeg (C++): Efficient audio and video merging.
MoviePy (Python): Pythonic video editing and subtitle integration.

Integrations

Airtable API: Data management and real-time updates.
Google Drive API: Media file storage and sharing.

Additional Libraries

libcurl, Boost.Asio, spdlog (C++): HTTP requests, async operations, and logging.
OpenCV, Tenacity (Python): Video processing and robust retries.

Installation and Setup
Prerequisites

Redis: Install and run Redis server (redis-server).
Airtable: Obtain an API key, base ID, and table name.
Google Drive: Set up API credentials with access to a target folder.

C++ Service Setup

Install Dependencies:
Crow, Redis++, libcurl, JsonCpp, LibTorch, ONNX Runtime, spdlog, Boost.
Use a package manager (e.g., apt, brew) or compile from source.


Compile:g++ -o automated automated.cpp -std=c++17 -I/path/to/headers -L/path/to/libs -lcrow -lredis++ -lcurl -ljsoncpp -ltorch -lonnxruntime -lspdlog -lboost_system


Run:./automated



Python Service Setup

Install Dependencies:pip install flask celery redis airtable-python-wrapper google-api-python-client torch transformers moviepy opencv-python tenacity


Configure Celery:Ensure Redis is running as the broker (redis://localhost:6379/0).
Run:python automated.py



Usage
The system is triggered via a /webhook endpoint accepting POST requests with JSON payloads.
Webhook Payload
{
  "action": "generateAudioVideo",
  "recordId": "rec1234567890"
}

Supported Actions

generateAudioVideo: Generates audio from an Airtable record’s text prompt and uploads it to Google Drive.
mergeAudioVideo: Merges audio and video from an Airtable record, adds subtitles via transcription, and uploads the final video.

Workflow

Send a POST request to /webhook with the desired action and record ID.
The task is queued and processed asynchronously.
Monitor progress and retrieve results via Airtable.

Examples

Audio Generation:

Send: {"action": "generateAudioVideo", "recordId": "rec123"}.
System generates audio using Tacotron 2 and WaveGlow, uploads it to Google Drive, and updates the Airtable record with the audio URL.


Video Merging with Subtitles:

Send: {"action": "mergeAudioVideo", "recordId": "rec123"}.
System downloads audio and video, transcribes audio with Whisper, merges them with FFmpeg/MoviePy, adds subtitles, uploads the result, and updates Airtable.



Contributing
Contributions are encouraged! To contribute:

Fork the repository.
Create a feature branch (git checkout -b feature-name).
Commit changes (git commit -m "Add feature").
Submit a pull request.

License
This project is licensed under the MIT License.
Acknowledgments

AI Models: Tacotron 2, WaveGlow (NVIDIA), Whisper (OpenAI).
Tools: FFmpeg, MoviePy, Airtable, Google Drive API.
Libraries: Crow, Flask, Celery, Redis, LibTorch, ONNX Runtime, Transformers.
