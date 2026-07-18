import os
import re
import csv
import sqlite3
from datetime import datetime

import cv2
import easyocr
from ultralytics import YOLO

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
VEHICLE_MODEL_PATH = "yolov8n.pt"
PLATE_MODEL_PATH = "models/plate_model.pt"
VIDEO_PATH = "data/videos/sample_video3.mp4"
OUTPUT_VIDEO_PATH = "output/results_video.mp4"
LOGS_CSV_PATH = "output/logs.csv"
DB_PATH = "database/traffic.db"
SCHEMA_PATH = "database/schema.sql"

VEHICLE_CLASSES = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}
LINE_Y = 240
CONFIDENCE_THRESHOLD = 0.4
PLATE_CONFIDENCE_THRESHOLD = 0.25
OCR_LANGUAGES = ["en"]
MIN_ACCEPTABLE_OCR_CONFIDENCE = 0.5  # once a track hits this, stop re-running OCR on it
OCR_EVERY_N_FRAMES = 5               # only attempt OCR every Nth frame per track
MAX_OCR_ATTEMPTS_PER_TRACK = 5       # give up on a track after this many tries

# ---------------------------------------------------------
# Setup: folders, database, models, OCR reader
# ---------------------------------------------------------
os.makedirs("output", exist_ok=True)
os.makedirs("database", exist_ok=True)

conn = sqlite3.connect(DB_PATH)
with open(SCHEMA_PATH, "r", encoding="utf-8-sig") as f:
    conn.executescript(f.read())
conn.commit()

vehicle_model = YOLO(VEHICLE_MODEL_PATH)
plate_model = YOLO(PLATE_MODEL_PATH)
reader = easyocr.Reader(OCR_LANGUAGES, gpu=False)

PLATE_TEXT_PATTERN = re.compile(r"[^A-Z0-9]")


def read_plate_text(plate_crop):
    """Run OCR on a cropped plate image. Returns (text, confidence)."""
    if plate_crop is None or plate_crop.size == 0:
        return None, 0.0
    gray = cv2.cvtColor(plate_crop, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    results = reader.readtext(gray)
    if not results:
        return None, 0.0
    best = max(results, key=lambda r: r[2])
    text = PLATE_TEXT_PATTERN.sub("", best[1].upper())
    return (text, best[2]) if text else (None, 0.0)


def detect_plate_in_vehicle(frame, vx1, vy1, vx2, vy2):
    """Look for a plate inside the vehicle's bounding box, return the plate crop."""
    vx1, vy1 = max(0, int(vx1)), max(0, int(vy1))
    vx2, vy2 = int(vx2), int(vy2)
    vehicle_crop = frame[vy1:vy2, vx1:vx2]
    if vehicle_crop.size == 0:
        return None

    plate_results = plate_model(vehicle_crop, conf=PLATE_CONFIDENCE_THRESHOLD, verbose=False)
    boxes = plate_results[0].boxes
    if len(boxes) == 0:
        return None

    best_box = max(boxes, key=lambda b: float(b.conf[0]))
    px1, py1, px2, py2 = best_box.xyxy[0].tolist()
    return vehicle_crop[int(py1):int(py2), int(px1):int(px2)]


def log_to_db_and_csv(vehicle_type, plate_number, timestamp):
    conn.execute(
        "INSERT INTO vehicle_logs (vehicle_type, plate_number, timestamp) VALUES (?, ?, ?)",
        (vehicle_type, plate_number, timestamp),
    )
    conn.commit()

    file_exists = os.path.isfile(LOGS_CSV_PATH)
    with open(LOGS_CSV_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["vehicle_type", "plate_number", "timestamp"])
        writer.writerow([vehicle_type, plate_number, timestamp])


# ---------------------------------------------------------
# Main loop
# ---------------------------------------------------------
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise FileNotFoundError(f"Video not found: {VIDEO_PATH}")

fps = cap.get(cv2.CAP_PROP_FPS) or 25
frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) // 2
frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) // 2
out_writer = cv2.VideoWriter(
    OUTPUT_VIDEO_PATH, cv2.VideoWriter_fourcc(*"mp4v"), fps, (frame_w, frame_h)
)

counted_ids = set()
class_counts = {name: 0 for name in VEHICLE_CLASSES.values()}
track_history = {}
best_plate_per_track = {}     # track_id -> (text, confidence)
ocr_attempts_per_track = {}   # track_id -> number of OCR attempts so far
frame_idx = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame_idx += 1
    if frame_idx % 50 == 0:
        print(f"Processing frame {frame_idx}...")

    results = vehicle_model.track(
        frame,
        classes=list(VEHICLE_CLASSES.keys()),
        conf=CONFIDENCE_THRESHOLD,
        persist=True,
        tracker="bytetrack.yaml",
        verbose=False,
    )

    annotated_frame = frame.copy()
    cv2.line(annotated_frame, (0, LINE_Y), (frame.shape[1], LINE_Y), (0, 0, 255), 2)

    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()
        track_ids = results[0].boxes.id.cpu().numpy().astype(int)
        class_ids = results[0].boxes.cls.cpu().numpy().astype(int)

        for box, track_id, cls_id in zip(boxes, track_ids, class_ids):
            x1, y1, x2, y2 = box
            cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
            class_name = VEHICLE_CLASSES.get(cls_id, "unknown")

            cv2.rectangle(annotated_frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"ID:{track_id} {class_name}", (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.circle(annotated_frame, (cx, cy), 4, (255, 0, 0), -1)

            # Try OCR at most every OCR_EVERY_N_FRAMES frames, and give up after
            # MAX_OCR_ATTEMPTS_PER_TRACK tries, or once a confident reading is found.
            attempts = ocr_attempts_per_track.get(track_id, 0)
            current_best_conf = best_plate_per_track.get(track_id, (None, 0.0))[1]
            if (
                current_best_conf < MIN_ACCEPTABLE_OCR_CONFIDENCE
                and attempts < MAX_OCR_ATTEMPTS_PER_TRACK
                and frame_idx % OCR_EVERY_N_FRAMES == 0
            ):
                plate_crop = detect_plate_in_vehicle(frame, x1, y1, x2, y2)
                text, conf = read_plate_text(plate_crop)
                if text and conf > current_best_conf:
                    best_plate_per_track[track_id] = (text, conf)
                ocr_attempts_per_track[track_id] = attempts + 1

            prev_cy = track_history.get(track_id)
            track_history[track_id] = cy

            if prev_cy is not None and track_id not in counted_ids:
                if prev_cy < LINE_Y <= cy:
                    counted_ids.add(track_id)
                    class_counts[class_name] += 1

                    plate_text = best_plate_per_track.get(track_id, (None, 0.0))[0]
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    log_to_db_and_csv(class_name, plate_text, timestamp)

                    label = plate_text if plate_text else "PLATE N/A"
                    cv2.putText(annotated_frame, label, (int(x1), int(y2) + 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)
                    print(f"[CROSSED] {class_name} | Plate: {label} | {timestamp}")

    y_offset = 30
    for class_name, count in class_counts.items():
        cv2.putText(annotated_frame, f"{class_name}: {count}", (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        y_offset += 30

    resized_frame = cv2.resize(annotated_frame, (frame_w, frame_h))
out_writer.write(resized_frame)

cap.release()
out_writer.release()
conn.close()

print("\nFinal Counts:")
for class_name, count in class_counts.items():
    print(f"{class_name}: {count}")
print(f"\nSaved: {OUTPUT_VIDEO_PATH}")
print(f"Saved: {LOGS_CSV_PATH}")
print(f"Saved: {DB_PATH}")