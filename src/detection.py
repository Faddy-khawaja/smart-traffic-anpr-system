from ultralytics import YOLO
import cv2

# Load pretrained YOLOv8 model (downloads automatically first time)
model = YOLO("yolov8n.pt")

# Path to your test video
video_path = "data/videos/sample_video1.mp4"
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Run detection on the frame
    results = model(frame, classes=[2, 3, 5, 7])  # car, motorcycle, bus, truck (COCO classes)
    annotated_frame = results[0].plot()

    cv2.imshow("Vehicle Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()