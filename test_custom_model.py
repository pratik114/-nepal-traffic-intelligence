import os
from ultralytics import YOLO

custom_model_path = os.path.join("models", "nepal_traffic_best.pt")

print("Testing custom model...")
print(f"Model path: {custom_model_path}")
print(f"Model exists: {os.path.exists(custom_model_path)}")

model = YOLO(custom_model_path)

print("\nModel class names:")
for cls_id, cls_name in model.names.items():
    print(f"  {cls_id}: {cls_name}")

print("\nModel loaded successfully!")
