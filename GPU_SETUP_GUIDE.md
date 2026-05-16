# NVIDIA GPU Setup Guide for Nepal Traffic Intelligence

## Prerequisites
- Windows 11
- NVIDIA GeForce GTX 1650
- NVIDIA Driver installed (we have v591.86)

## Step 1: Create a Virtual Environment with Compatible Python
We're using Python 3.13 (compatible with PyTorch CUDA builds):
```powershell
py -3.13 -m venv venv
.\venv\Scripts\Activate.ps1
```

## Step 2: Install CUDA‑Enabled PyTorch
Install PyTorch with CUDA 12.4 support:
```powershell
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
```

## Step 3: Install Other Dependencies
```powershell
python -m pip install ultralytics opencv-python numpy
```

## Step 4: Verify GPU Setup
Run the verification script:
```powershell
python verify_gpu.py
```

### Expected Output:
```
======================================================================
Nepal Traffic Intelligence - GPU Verification
======================================================================

1. Environment Info
------------------------------
Python version: 3.13.x
PyTorch version: 2.6.0+cu124
PyTorch CUDA version: 12.4

2. CUDA Availability Check
------------------------------
CUDA available: True
CUDA device count: 1
  GPU 0: NVIDIA GeForce GTX 1650
  Total memory: 4.00 GB

3. GPU Inference Test (YOLOv8n)
------------------------------
✓ YOLO inference successful on cuda!
  Number of detections: X

======================================================================
Verification complete!
======================================================================
```

## Step 5: Run the Project with GPU
```powershell
python main.py
```
Our `VehicleDetector` class automatically uses GPU (`device="auto"`) and falls back to CPU if CUDA is unavailable!

## Troubleshooting
- If `torch.cuda.is_available()` returns False:
  - Make sure you're using the virtual environment: `.\venv\Scripts\Activate.ps1`
  - Verify you installed the CUDA version of PyTorch (not +cpu)
  - Check NVIDIA driver installation with `nvidia-smi`
- For Jetson Nano deployment (future):
  - Use NVIDIA JetPack SDK which includes pre‑built PyTorch with CUDA for Jetson
