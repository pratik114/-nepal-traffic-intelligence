import os
import torch
from ultralytics import YOLO
from training.utils import split_dataset


def train_model(
    labeled_dir="dataset/labeled",
    dataset_dir="dataset",
    models_dir="dataset/models",
    model_name="yolov8n.pt",
    epochs=100,
    batch_size=16,
    img_size=640,
    resume=False
):
    os.makedirs(models_dir, exist_ok=True)

    data_yaml = split_dataset(labeled_dir, dataset_dir)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    model = YOLO(model_name)

    results = model.train(
        data=data_yaml,
        epochs=epochs,
        batch=batch_size,
        imgsz=img_size,
        device=device,
        project=models_dir,
        name="nepal_traffic",
        exist_ok=True,
        resume=resume
    )

    best_model_path = os.path.join(models_dir, "nepal_traffic", "weights", "best.pt")
    last_model_path = os.path.join(models_dir, "nepal_traffic", "weights", "last.pt")
    print(f"\nTraining complete!")
    print(f"Best model saved to: {best_model_path}")
    print(f"Last model saved to: {last_model_path}")

    return best_model_path, last_model_path


if __name__ == "__main__":
    train_model()
