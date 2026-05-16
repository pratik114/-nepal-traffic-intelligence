import sys
import torch
import cv2
from ultralytics import YOLO
import numpy as np

def main():
    print("=" * 70)
    print("Nepal Traffic Intelligence - GPU Verification")
    print("=" * 70)

    print("\n1. Environment Info")
    print("-" * 30)
    print(f"Python version: {sys.version}")
    print(f"PyTorch version: {torch.__version__}")
    if torch.version.cuda:
        print(f"PyTorch CUDA version: {torch.version.cuda}")

    print("\n2. CUDA Availability Check")
    print("-" * 30)
    cuda_available = torch.cuda.is_available()
    print(f"CUDA available: {cuda_available}")
    if cuda_available:
        print(f"CUDA device count: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
            print(f"  Total memory: {torch.cuda.get_device_properties(i).total_memory / 1024**3:.2f} GB")
        device = torch.device("cuda")
    else:
        print("  Using CPU (fallback)")
        device = torch.device("cpu")

    print("\n3. GPU Inference Test (YOLOv8n)")
    print("-" * 30)
    try:
        model = YOLO("yolov8n.pt")
        dummy_image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
        results = model(dummy_image, device=device, verbose=False)
        print(f"✓ YOLO inference successful on {device}!")
        print(f"  Number of detections: {len(results[0].boxes)}")
    except Exception as e:
        print(f"✗ YOLO inference failed: {e}")

    print("\n" + "=" * 70)
    print("Verification complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
