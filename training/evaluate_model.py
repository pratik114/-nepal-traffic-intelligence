import os
import time
from pathlib import Path
import torch
import cv2
import numpy as np
from ultralytics import YOLO


def evaluate_model(
    model_path="models/nepal_traffic_best.pt",
    dataset_yaml="dataset/labeled/dataset.yaml",
    output_dir="training/runs/evaluation"
):
    print("=" * 80)
    print("NEPAL TRAFFIC MODEL EVALUATION")
    print("=" * 80)

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    samples_dir = Path(output_dir) / "samples"
    samples_dir.mkdir(parents=True, exist_ok=True)

    device = "0" if torch.cuda.is_available() else "cpu"
    print(f"\nLoading model from: {model_path}")
    model = YOLO(model_path)
    class_names = model.names
    print(f"Model loaded! Classes: {list(class_names.values())}")
    print(f"Using device: {device}")

    print("\n" + "-" * 80)
    print("TEST SET EVALUATION")
    print("-" * 80)
    metrics = model.val(
        data=dataset_yaml,
        split="test",
        device=device,
        project=output_dir,
        name="test_eval",
        exist_ok=True,
        plots=True
    )

    print("\nPER-CLASS METRICS:")
    print("-" * 80)
    print(f"{'Class':<15} {'Precision':<10} {'Recall':<10} {'mAP50':<10} {'mAP50-95':<10}")
    print("-" * 80)
    for idx, name in class_names.items():
        p = metrics.box.mp[idx] if idx < len(metrics.box.mp) else 0
        r = metrics.box.mr[idx] if idx < len(metrics.box.mr) else 0
        map50 = metrics.box.map50
        map50_95 = metrics.box.map
        print(f"{name:<15} {p:<10.3f} {r:<10.3f} {map50:<10.3f} {map50_95:<10.3f}")

    print("\n" + "-" * 80)
    print("INFERENCE SPEED TEST")
    print("-" * 80)
    test_image = list(Path("dataset/labeled/images/test").iterdir())[0]
    img = cv2.imread(str(test_image))

    for device_name, dev in [("GPU", "0"), ("CPU", "cpu")]:
        if device_name == "GPU" and not torch.cuda.is_available():
            print(f"{device_name}: Not available")
            continue
        
        model.to(dev)
        num_runs = 100
        start_time = time.time()
        for _ in range(num_runs):
            _ = model.predict(img, device=dev, verbose=False)
        elapsed = time.time() - start_time
        fps = num_runs / elapsed
        print(f"{device_name} FPS: {fps:.1f} (inference time: {(1000/fps):.1f} ms)")

    print("\n" + "-" * 80)
    print("SAMPLE PREDICTIONS")
    print("-" * 80)
    test_images = list(Path("dataset/labeled/images/test").iterdir())[:5]
    for i, img_path in enumerate(test_images):
        img = cv2.imread(str(img_path))
        results = model.predict(img, device=device, verbose=False)
        
        annotated_img = results[0].plot()
        output_path = samples_dir / f"sample_{i+1}.jpg"
        cv2.imwrite(str(output_path), annotated_img)
        print(f"Sample {i+1}: Saved to {output_path}")

    print("\n" + "=" * 80)
    print("EVALUATION COMPLETE")
    print("=" * 80)
    print(f"Results saved to: {output_dir}")
    return metrics


if __name__ == "__main__":
    evaluate_model()
