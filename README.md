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
- 

---
Video Input (CCTV / Recorded Footage)
│
▼
Frame Extraction (OpenCV)
│
▼
YOLOv8 Vehicle Detection  ──►  ByteTrack Multi-Object Tracking
│
▼
Virtual Line-Crossing Detection  ──►  Class-wise Vehicle Counter
│
▼
Custom YOLOv8 License Plate Detector
│
▼
EasyOCR Text Recognition
│
▼
SQLite Database  +  CSV Logs
│
▼
Streamlit Analytics Dashboard
---

## Tech Stack

| Component            | Technology              |
|-----------------------|--------------------------|
| Vehicle Detection      | YOLOv8 (Ultralytics)     |
| Object Tracking         | ByteTrack                |
| Plate Detection         | Custom fine-tuned YOLOv8 |
| OCR                      | EasyOCR                  |
| Database                 | SQLite                   |
| Dashboard                | Streamlit + Plotly       |
| Core Language              | Python 3.12              |

---

## Model Performance

The license plate detection model was fine-tuned on a 30,000-image subset of a public license plate dataset:

| Metric        | Score  |
|----------------|--------|
| mAP50          | 94.2%  |
| Precision      | 96.2%  |
| Recall         | 90.4%  |
| Training time  | ~40 minutes (5 epochs, Tesla T4 GPU) |

---

## Project Structure
smart-traffic-anpr-system/
├── data/videos/            # Sample traffic footage for testing
├── models/                 # Trained model weights (plate_model.pt)
├── src/
│   ├── detection.py        # Standalone vehicle detection test script
│   ├── anpr_pipeline.py    # Full pipeline: detection + tracking + OCR + logging
│   └── compress_video.py   # Utility to compress output demo videos
├── database/
│   └── schema.sql          # SQLite schema for vehicle_logs table
├── app/
│   └── streamlit_app.py    # Live analytics dashboard
├── demo/                   # Demo video assets
├── output/                 # Generated results (video, logs.csv)
├── requirements.txt
└── README.md
---

## Getting Started

### 1. Install dependencies

pip install -r requirements.txt

### 2. Run the full detection + ANPR pipeline

python src/anpr_pipeline.py

This processes a video from `data/videos/`, detects and tracks vehicles, counts them on line-crossing, detects and reads license plates, and logs everything to `database/traffic.db` and `output/logs.csv`.

### 3. Launch the live dashboard

streamlit run app/streamlit_app.py

View live class-wise vehicle counts, license plate logs, traffic analytics charts, and export historical reports as CSV.

---

## Roadmap

- [ ] Improve OCR accuracy with plate-region super-resolution preprocessing
- [ ] Multi-camera support with cross-camera deduplication
- [ ] REST API service (FastAPI) for integration with external traffic systems
- [ ] Deploy on edge devices (NVIDIA Jetson) for on-site inference
- [ ] Containerize with Docker for production deployment

---

## License

This project uses a publicly available license plate dataset (CC BY 4.0) from Roboflow Universe for model training.



## System Architecture
