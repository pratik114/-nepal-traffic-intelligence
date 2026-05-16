import torch
import os
import cv2
from ultralytics import YOLO


class VehicleDetector:
    def __init__(self, model_name=None, device="auto"):
        self.device = self._get_device(device)
        print(f"Using device: {self.device}")
        
        if model_name is None:
            custom_paths = [
                os.path.join("runs", "detect", "training", "runs", "nepal_traffic_v1", "weights", "best.pt"),
                os.path.join("models", "nepal_traffic_best.pt"),
                os.path.join("runs", "detect", "runs", "roboflow_traffic", "weights", "best.pt")
            ]
            model_name = "yolov8n.pt"
            use_default = True  # Set to False to use custom models
            
            if not use_default:
                for path in custom_paths:
                    if os.path.exists(path):
                        model_name = path
                        print(f"Using custom traffic model: {model_name}")
                        break
            
            if model_name == "yolov8n.pt":
                print(f"Using default YOLOv8 model: {model_name}")
        
        self.model = YOLO(model_name)
        print(f"Model loaded successfully!")
        print(f"Model classes: {self.model.names}")
        
        nepal_mapping = {
            'car': 'car',
            'motorcycle': 'motorcycle',
            'bus': 'bus',
            'truck': 'truck',
            'microbus': 'bus'
        }
        
        roboflow_mapping = {
            'big bus': 'bus',
            'big truck': 'truck',
            'bus-l-': 'bus',
            'bus-s-': 'bus',
            'car': 'car',
            'mid truck': 'truck',
            'small bus': 'bus',
            'small truck': 'truck',
            'truck-l-': 'truck',
            'truck-m-': 'truck',
            'truck-s-': 'truck',
            'truck-xl-': 'truck'
        }
        
        coco_mapping = {
            'car': 'car',
            'motorcycle': 'motorcycle',
            'bus': 'bus',
            'truck': 'truck'
        }
        
        model_class_names = list(self.model.names.values())
        
        if 'microbus' in model_class_names:
            self.class_mapping = nepal_mapping
            print("Using Nepal traffic class mapping")
        elif 'big bus' in model_class_names:
            self.class_mapping = roboflow_mapping
            print("Using Roboflow class mapping")
        else:
            self.class_mapping = coco_mapping
            print("Using COCO class mapping")
        
        self.classes_of_interest = list(self.class_mapping.keys())
        
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def _get_device(self, device):
        if device == "auto":
            if torch.cuda.is_available():
                return "cuda"
            elif torch.backends.mps.is_available():
                return "mps"
            else:
                return "cpu"
        return device

    def detect_and_track(self, frame, conf_threshold=0.3):
        results = self.model.track(
            frame, 
            conf=conf_threshold, 
            device=self.device, 
            verbose=False,
            persist=True,
            tracker="bytetrack.yaml"
        )
        detections = []
        tracked_objects = {}
        
        for result in results:
            if result.boxes is not None and result.boxes.id is not None:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    class_name = self.model.names[class_id]
                    if class_name in self.classes_of_interest:
                        track_id = int(box.id[0])
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        confidence = float(box.conf[0])
                        mapped_class = self.class_mapping.get(class_name, class_name)
                        detections.append({
                            "bbox": [x1, y1, x2, y2],
                            "class": mapped_class,
                            "confidence": confidence,
                            "track_id": track_id
                        })
                        tracked_objects[track_id] = {
                            "centroid": ((x1 + x2) / 2, (y1 + y2) / 2),
                            "class": mapped_class,
                            "bbox": [x1, y1, x2, y2]
                        }
        
        return detections, tracked_objects
    
    def detect_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        face_boxes = []
        for (x, y, w, h) in faces:
            face_boxes.append([x, y, x + w, y + h])
        return face_boxes
