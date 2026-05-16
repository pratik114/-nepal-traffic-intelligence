import os
import torch
from ultralytics import YOLO


def evaluate_model(
    model_path="dataset/models/nepal_traffic/weights/best.pt",
    data_yaml="dataset/data.yaml",
    output_dir="dataset/models/nepal_traffic"
):
    os.makedirs(output_dir, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    model = YOLO(model_path)
    results = model.val(
        data=data_yaml,
        device=device,
        project=output_dir,
        name="evaluation",
        exist_ok=True
    )

    print("\nEvaluation Results:")
    print(f"Precision: {results.box.mp:.4f}")
    print(f"Recall: {results.box.mr:.4f}")
    print(f"mAP50: {results.box.map50:.4f}")
    print(f"mAP50-95: {results.box.map:.4f}")

    return results


if __name__ == "__main__":
    evaluate_model()
