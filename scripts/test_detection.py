from ultralytics import YOLO 
import cv2 
import os

os.makedirs("scripts", exist_ok=True)

model = YOLO("models/nepal_traffic_best.pt") 
print(f"Model classes: {model.names}") 

cap = cv2.VideoCapture("videos/input.mp4") 
for i in range(10): 
    ret, frame = cap.read() 
    if not ret: break 
    results = model(frame, conf=0.20, verbose=False)[0] 
    print(f"Frame {i+1}: {len(results.boxes)} detections") 
    for box in results.boxes: 
        cls = int(box.cls[0]) 
        conf = float(box.conf[0]) 
        print(f"  Class {cls} ({model.names[cls]}): {conf:.2f}") 
cap.release()
