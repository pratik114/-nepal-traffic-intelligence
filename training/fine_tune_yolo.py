import os
import time
import shutil
from pathlib import Path
import torch
from ultralytics import YOLO


def check_gpu_memory():
    if torch.cuda.is_available():
        device = torch.device("cuda")
        total_mem = torch.cuda.get_device_properties(device).total_memory / 1024**3
        used_mem = torch.cuda.memory_allocated(device) / 1024**3
        free_mem = total_mem - used_mem
        print(f"GPU Memory Check: {torch.cuda.get_device_name(0)}")
        print(f"  Total: {total_mem:.2f} GB")
        print(f"  Used:  {used_mem:.2f} GB")
        print(f"  Free:  {free_mem:.2f} GB")
        return free_mem >= 2.0
    else:
        print("GPU not available, using CPU")
        return False


def fine_tune_yolo(
    dataset_yaml="dataset/labeled/dataset.yaml",
    base_model="yolov8n.pt",
    epochs=50,
    img_size=640,
    batch_size=8,
    patience=10,
    project_dir="training/runs",
    run_name="nepal_traffic_v1"
):
    print("=" * 80)
    print("NEPAL TRAFFIC YOLO FINE-TUNING")
    print("=" * 80)

    if not check_gpu_memory():
        print("Warning: Less than 2 GB free GPU memory, consider reducing batch size!")

    device = "0" if torch.cuda.is_available() else "cpu"
    print(f"\nUsing device: {device}")

    Path(project_dir).mkdir(parents=True, exist_ok=True)
    Path("models").mkdir(exist_ok=True)

    model = YOLO(base_model)

    start_time = time.time()
    print(f"\nStarting training for {epochs} epochs...")
    results = model.train(
        data=dataset_yaml,
        epochs=epochs,
        imgsz=img_size,
        batch=batch_size,
        device=device,
        optimizer="AdamW",
        patience=patience,
        project=project_dir,
        name=run_name,
        exist_ok=True,
        plots=True,
        save=True,
        fliplr=0.5,
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,
        mosaic=1.0
    )
    training_time = time.time() - start_time

    best_model_path = Path(project_dir) / run_name / "weights" / "best.pt"
    target_model_path = Path("models") / "nepal_traffic_best.pt"
    if best_model_path.exists():
        shutil.copy(best_model_path, target_model_path)
        print(f"\nBest model copied to: {target_model_path}")
    else:
        print("\nWarning: Could not find best model!")

    print("\n" + "=" * 80)
    print("TRAINING COMPLETE")
    print("=" * 80)
    print(f"Training time: {training_time/60:.1f} minutes ({training_time:.0f} seconds)")

    try:
        metrics = model.val(data=dataset_yaml, split="val")
        print("\nVALIDATION RESULTS:")
        print(f"  mAP50-95: {metrics.box.map:.4f}")
        print(f"  mAP50:    {metrics.box.map50:.4f}")
        print(f"  Precision: {metrics.box.mp:.4f}")
        print(f"  Recall:    {metrics.box.mr:.4f}")
    except Exception as e:
        print(f"\nWarning: Could not run final validation: {e}")

    print("=" * 80)
    return results


if __name__ == "__main__":
    fine_tune_yolo()
