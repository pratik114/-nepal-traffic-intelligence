import os
import sys
sys.path.insert(0, '.')

from training.train import train_model

print("=== Starting Training Pipeline ===")
try:
    best_path, last_path = train_model(
        labeled_dir="dataset/labeled",
        dataset_dir="dataset",
        models_dir="dataset/models",
        model_name="yolov8n.pt",
        epochs=5,
        batch_size=4,
        img_size=320
    )
    print(f"\n=== Training Complete! ===")
    print(f"Best model: {best_path}")
    print(f"Last model: {last_path}")
except Exception as e:
    print(f"Training error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
