# 🚦 Smart City Traffic ANPR System

AI-powered, production-grade traffic monitoring system that performs real-time vehicle detection, multi-object tracking, line-crossing based counting, and automated license plate recognition (ANPR) — built for smart city surveillance and law enforcement applications.

---

## Demo Video

https://github.com/user-attachments/assets/63b72f52-9a12-4473-b25d-a1ac0b7bd599

The video above shows the complete pipeline running end-to-end: vehicle detection and tracking, virtual line-crossing counts, and automatic license plate recognition on live traffic footage.

---

## Key Features

- **Real-time vehicle detection** — cars, motorcycles, buses, and trucks detected using YOLOv8
- **Multi-object tracking** — ByteTrack assigns a persistent unique ID to every vehicle, preventing duplicate counts
- **Virtual line-crossing counter** — class-wise vehicle counts triggered by centroid crossing detection
- **Custom-trained ANPR model** — a YOLOv8 model fine-tuned on a 30,000+ image license plate dataset (94.2% mAP50)
- **OCR-based plate recognition** — EasyOCR extracts plate text from detected plate regions, with confidence-based retry logic to avoid wasting compute on every frame
- **Persistent logging** — every crossing event is logged to a SQLite database and a CSV file with vehicle type, plate number, and timestamp
- **Live analytics dashboard** — a Streamlit dashboard for live counts, plate logs, traffic trend charts, and CSV export

---

## System Architecture
