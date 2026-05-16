import os
import torch
from ultralytics import YOLO


def train_roboflow_model():
    data_yaml_path = os.path.join("dataset", "labeled", "data.yaml")
    
    print(f"Training YOLOv8 model on Roboflow dataset...")
    print(f"Data YAML: {data_yaml_path}")
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    model = YOLO("yolov8n.pt")
    
    results = model.train(
        data=data_yaml_path,
        epochs=50,
        batch=8,
        imgsz=640,
        device=device,
        project="runs",
        name="roboflow_traffic",
        exist_ok=True
    )
    
    best_model_path = os.path.join("runs", "roboflow_traffic", "weights", "best.pt")
    last_model_path = os.path.join("runs", "roboflow_traffic", "weights", "last.pt")
    
    print(f"\nTraining complete!")
    print(f"Best model saved to: {best_model_path}")
    print(f"Last model saved to: {last_model_path}")
    
    if os.path.exists(best_model_path):
        import shutil
        shutil.copy(best_model_path, os.path.join("models", "nepal_traffic_best.pt"))
        print(f"Copied best model to: models/nepal_traffic_best.pt")
    
    return best_model_path, last_model_path


if __name__ == "__main__":
    train_roboflow_model()
