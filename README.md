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
[View raw](https://github.com/Faddy-khawaja/smart-traffic-anpr-system/raw/refs/heads/main/demo/anpr-demo.mp4)
(Sorry about that, but we can’t show files that are this big right now.)


Diagnosed video hosting constraints and devised alternative upload solution
Diagnosed video hosting constraints and devised alternative upload solution
Achha, ye samajh aa gaya — GitHub ke normal repo blob preview ka video-specific limit 25MB se kam hai (asal mein kaafi chhota, kabhi kabhi ~10MB ke qareeb), aur kabhi kabhi cache/rendering issues bhi hote hain jo consistently kaam nahi karte, chahe file chhoti ho.

Achi khabar: Iska matlab ye nahi hai ke kuch bigड़ा hai — video file poori tarah sahi hai, sirf GitHub ka built-in preview player thoda unreliable hai videos ke sath. Iska ek behtar solution hai jo professional projects mein bhi use hota hai.

Behtar Solution: GitHub Issue Se Video Upload Karo (Reliable Embed Milta Hai)
Ye ek known trick hai — GitHub ke Issues/Discussions ka drag-and-drop uploader videos ko unke CDN (user-images) pe daalta hai, jo hamesha reliably play hota hai, chahe README mein embed karo.

Step 1: Naya Issue Banao (Temporary, Baad Mein Close Kar Denge)
Apni repo pe jao: github.com/Faddy-khawaja/smart-traffic-anpr-system
Upar "Issues" tab pe click karo
"New Issue" button dabao
Step 2: Video Drag-Drop Karo
Issue ke description wale text box mein click karo
Apni video file (demo/traffic-anpr-detection-demo.mp4) ko File Explorer se drag karke us text box mein drop karo (ya "attach files" click karke select karo)
Thoda wait karo — GitHub upload karega aur ek link generate karega, jaisa:
https://github.com/user-attachments/assets/xxxxx-xxxxx
Step 3: Wo Link Copy Karo
Jo link box mein appear ho (upload complete hone ke baad), use copy kar lo.

Step 4: Issue Ko Submit Kiye Bina Chhod Do (Ya Submit Karke Baad Mein Close Kar Do)
Issue submit karne ki zarurat nahi — bas link mil jaye kaafi hai. Agar chahen to issue ko cancel kar dena, link phir bhi kaam karega.

Step 5: README Mein Ye Naya Link Daalo
README.md mein purani line:

markdown
Video: demo/traffic-anpr-detection-demo.mp4
Isse replace karo:

markdown
## Demo Video

https://github.com/user-attachments/assets/xxxxx-xxxxx
(apna asal link daalo)

Save karo, phir push karo:

git add .
git commit -m "Use GitHub CDN link for reliable video embed"
git push origin main
Ye tareeqa try karo — ye videos ke liye GitHub ka sabse reliable embed method hai. Batao Issues tab mil gaya aur upload ho gaya, phir link mujhe bhej dena taake README update kar sakein.

sahi batao kia kia kerna hai


Tayyar kiya step-by-step checklist video masla hal karne ke liye
Tayyar kiya step-by-step checklist video masla hal karne ke liye
Theek hai, bilkul seedhe seedhe steps — order se, ek-ek kaam.

Step 1: Browser Mein GitHub Repo Kholo
Address bar mein:

github.com/Faddy-khawaja/smart-traffic-anpr-system
Step 2: "Issues" Tab Pe Jao
Repo ke upar menu mein "Issues" likha hoga — us par click karo.

Step 3: Naya Issue Banao
"New Issue" ya "New" button dabao (green button hota hai).

Step 4: Description Box Mein Click Karo
Ek bada text box khulega jahan likha hoga "Leave a comment" ya "Write". Us box ke andar click karo (cursor blink hona chahiye).

Step 5: Video Ko Drag-Drop Karo
File Explorer kholo (Windows key + E)
Apni video dhoondo:
C:\Users\kk\Desktop\my_new_project\my_new_project\demo\traffic-anpr-detection-demo.mp4
Us file ko mouse se pakड़ो (click aur hold karo), phir browser wale text box mein le jao aur drop kar do (chhod do)
Step 6: Upload Hone Ka Wait Karo
Thoda progress dikhega ("Uploading..."). Complete hone pe text box mein automatically ek link paste ho jayega, kuch aisa:

https://github.com/user-attachments/assets/abc123-xyz456
Step 7: Wo Link Copy Karo
Us poore link ko select karo (mouse se drag karke highlight karo), Ctrl+C dabao.

Step 8: Wo Link Yahan Mujhe Bhej Do
Bas is link ko yahan paste kar do (Issue submit karne ki zarurat nahi) — main aapko batunga README mein exact kahan aur kaise daalna hai.

Step 5 tak pahunch kar batao video upload ho gayi aur link mil gaya — ya agar kahin atak jao (jaise drag-drop kaam na kare), wahan exactly bata dena kya dikh raha hai.

box keh andher bhi daldia tha 
https://github.com/user-attachments/assets/63b72f52-9a12-4473-b25d-a1ac0b7bd599
webadrres peh bhi daldia 
https://github.com/user-attachments/assets/63b72f52-9a12-4473-b25d-a1ac0b7bd599

Perfect! ✅ Link mil gaya:

https://github.com/user-attachments/assets/63b72f52-9a12-4473-b25d-a1ac0b7bd599
Ye GitHub ka reliable CDN link hai — is se video har jagah play hogi, chahe README mein ho ya seedha browser mein khol ke dekho.

Ab README Update Karo
Step 1: README.md Kholo VS Code Mein
Left panel se README.md pe click karo.

Step 2: Purani Video Line Dhoondo
Ye line dhoondo (jo pehle likhi thi):

Video: demo/traffic-anpr-detection-demo.mp4
Step 3: Replace Karo
Isse replace karo:

## Demo Video

https://github.com/user-attachments/assets/63b72f52-9a12-4473-b25d-a1ac0b7bd599
Step 4: Save Karo
Ctrl + S

Ab Push Karo
Terminal mein:

git add .
git commit -m "Use reliable GitHub CDN link for demo video"
git push origin main
Ye karo aur batao ho gaya — phir hum browser mein README refresh karke confirm karenge video ab reliably play ho rahi hai.

zara industrial level ka bhi bana doh readme aur play hohgae readme pay


Orchestrated professional README with embedded video playback
Orchestrated professional README with embedded video playback
Bilkul! Chalo ek professional, industrial-level README banate hain jo client ko pura confidence de — architecture, results, setup, sab kuch clearly dikhega.

Step 1: README.md Kholo VS Code Mein
Left panel se README.md pe click karo.

Step 2: Poora Purana Content Delete Karo
Editor ke andar click karo, Ctrl+A dabao (sab select ho jayega), phir Delete dabao (khaali ho jayega).

Step 3: Ye Poora Naya Content Paste Karo
markdown
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
Video Input (CCTV / Recorded Footage)
│
▼
Frame Extraction (OpenCV)
│
▼
YOLOv8 Vehicle Detection ──► ByteTrack Multi-Object Tracking
│
▼
Virtual Line-Crossing Detection ──► Class-wise Vehicle Counter
│
▼
Custom YOLOv8 License Plate Detector
│
▼
EasyOCR Text Recognition
│
▼
SQLite Database + CSV Logs
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
├── data/videos/ # Sample traffic footage for testing
├── models/ # Trained model weights (plate_model.pt)
├── src/
│ ├── detection.py # Standalone vehicle detection test script
│ ├── anpr_pipeline.py # Full pipeline: detection + tracking + OCR + logging
│ └── compress_video.py # Utility to compress output demo videos
├── database/
│ └── schema.sql # SQLite schema for vehicle_logs table
├── app/
│ └── streamlit_app.py # Live analytics dashboard
├── demo/ # Demo video assets
├── output/ # Generated results (video, logs.csv)
├── requirements.txt
└── README.md
---

## Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the full detection + ANPR pipeline

```bash
python src/anpr_pipeline.py
```

This processes a video from `data/videos/`, detects and tracks vehicles, counts them on line-crossing, detects and reads license plates, and logs everything to `database/traffic.db` and `output/logs.csv`.

### 3. Launch the live dashboard

```bash
streamlit run app/streamlit_app.py
```

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
