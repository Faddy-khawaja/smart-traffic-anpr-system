# Smart City Traffic ANPR System

AI-powered smart city traffic monitoring system using YOLOv8 for vehicle detection, ByteTrack for tracking, and OCR for automated license plate recognition (ANPR).

## Features

- Real-time vehicle detection (car, motorcycle, bus, truck) using YOLOv8
- Multi-object tracking with ByteTrack (unique ID per vehicle)
- Class-wise vehicle counting via virtual line-crossing detection
- Custom-trained YOLOv8 model for license plate detection
- OCR-based plate text recognition using EasyOCR
- Automatic logging to SQLite database and CSV
- Live analytics dashboard built with Streamlit

## Demo

Watch the system in action — vehicle detection, tracking, line-crossing counting, and automatic license plate recognition:

## Demo Video

https://github.com/user-attachments/assets/63b72f52-9a12-4473-b25d-a1ac0b7bd599

This demo shows:
- Real-time vehicle detection and tracking (YOLOv8 + ByteTrack)
- Class-wise vehicle counting as vehicles cross a virtual line
- Automatic license plate detection using a custom-trained YOLOv8 model
- OCR-based plate text recognition (EasyOCR)
- Live logging to SQLite database

## Tech Stack

Python, OpenCV, YOLOv8, ByteTrack, EasyOCR, SQLite, Streamlit

## How to Run

1. Install dependencies: pip install -r requirements.txt
2. Run the full pipeline: python src/anpr_pipeline.py
3. Launch the dashboard: streamlit run app/streamlit_app.py
