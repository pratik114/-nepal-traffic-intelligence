# Nepal Traffic Intelligence - Jetson Nano Deployment Guide

This guide will help you deploy the Nepal Traffic Intelligence MVP on NVIDIA Jetson Nano!

## Prerequisites
- NVIDIA Jetson Nano Developer Kit
- microSD Card (64GB+ Class 10 recommended
- NVIDIA JetPack 4.6.1 or newer
- Power supply (5V 4A recommended
- USB webcam or camera module
- Keyboard, mouse, monitor (for initial setup)

## Step 1: Flash JetPack to microSD Card
1. Download NVIDIA JetPack SDK from NVIDIA's website
2. Use BalenaEtcher to flash JetPack to your microSD card
3. Insert microSD card into Jetson Nano and power on
4. Complete initial setup (language, timezone, user account, network)

## Step 2: Install System Dependencies
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git cmake libopencv-dev -y
```

## Step 3: Create Python Virtual Environment
```bash
cd ~
python3 -m venv traffic-venv
source traffic-venv/bin/activate
```

## Step 4: Install PyTorch for Jetson
NVIDIA provides pre-built PyTorch for Jetson!
```bash
# For JetPack 4.6.1 (L4T 32.7.1)
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/l4t
```

## Step 5: Clone Project Dependencies
```bash
cd ~
git clone <your-repo-url> nepal-traffic-intelligence
cd nepal-traffic-intelligence
pip install -r requirements.txt
```

## Step 6: Run the System
```bash
# Activate venv
source ~/traffic-venv/bin/activate

# Set USE_CAMERA=True in main.py
python main.py

# In another terminal, run frontend
cd frontend
npm install
npm run dev
```

## Optimization Tips for Jetson Nano
1. Use yolov8n.pt (nano version, smallest/fastest)
2. Set MAX_WIDTH to 960 or 720 for better performance
3. Reduce CONF_THRESHOLD to 0.4 to reduce false positives
4. Use TensorRT for YOLO export:
```bash
yolo export model=yolov8n.pt format=engine
```
Then update VehicleDetector to use yolov8n.engine!

## Troubleshooting Jetson Nano
- If PyTorch not compiled without CUDA: use NVIDIA's pre-built wheels!
- Low FPS: reduce MAX_WIDTH!
