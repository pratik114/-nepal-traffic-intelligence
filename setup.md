# 🛠️ Setup Guide

This guide will help you set up Nepal Traffic Intelligence on your local machine.

## 📋 Prerequisites

- **Python 3.13 or higher**
- **Node.js 18 or higher**
- **Git**
- **NVIDIA GPU** (recommended for faster inference)
- **CUDA Toolkit** (if using NVIDIA GPU)

## 🔧 Backend Setup

### 1. Clone the Repository

```bash
git clone https://github.com/pratik114/nepal-traffic-intelligence.git
cd nepal-traffic-intelligence
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify GPU (Optional but Recommended)

```bash
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

## 🎨 Frontend Setup

```bash
cd frontend
npm install
```

## ⚙️ Configuration

### 1. Add Input Video

Place your video file in the `videos/` folder:
```
videos/
└── input.mp4
```

### 2. Configure Main Settings (Optional)

Edit `main.py` to change settings:
- `USE_CAMERA`: Set to `True` to use webcam instead of video file
- `DEFAULT_VIDEO`: Name of your input video file
- `CONF_THRESHOLD`: Confidence threshold for detection (0.1 - 1.0)

## 🤖 Download Trained Model

The trained model is not included in the repository due to file size. You have two options:

### Option 1: Train Your Own Model
See [TRAINING.md](TRAINING.md) for detailed instructions.

### Option 2: Download Pre-trained Model
1. Visit the [Releases page](https://github.com/pratik114/nepal-traffic-intelligence/releases)
2. Download `nepal_traffic_best.pt`
3. Place it in the `models/` folder:
   ```
   models/
   └── nepal_traffic_best.pt
   ```

## 🚀 Running the System

### 1. Start Backend

In one terminal:
```bash
python main.py
```

You should see:
```
FastAPI server running at http://localhost:8000
Traffic live endpoint: http://localhost:8000/traffic/live
Traffic stream endpoint: http://localhost:8000/traffic/stream
```

### 2. Start Frontend

In another terminal:
```bash
cd frontend
npm run dev
```

You should see:
```
VITE v5.x.x ready in xxx ms
Local: http://localhost:3000/
```

### 3. Open Dashboard

Open your browser and visit: **http://localhost:3000**

## 🔍 Troubleshooting

### CUDA Not Detected

**Problem:** `CUDA available: False`

**Solution:**
1. Install NVIDIA CUDA Toolkit
2. Install PyTorch with CUDA support:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   ```

### Video File Not Found

**Problem:** Error saying "No MP4 videos found in videos/ folder!"

**Solution:**
1. Create a `videos/` folder in project root
2. Place your MP4 video file inside
3. Make sure the filename matches `DEFAULT_VIDEO` in `main.py`

### Model Not Loading

**Problem:** Model file not found

**Solution:**
1. Check that `nepal_traffic_best.pt` is in the `models/` folder
2. If not, train your own or download from Releases

### Stream Not Displaying

**Problem:** Dashboard shows "Connecting to stream..." forever

**Solution:**
1. Verify backend is running at http://localhost:8000
2. Check backend logs for errors
3. Try opening stream directly: http://localhost:8000/traffic/stream
4. Clear browser cache and refresh

### Port Already in Use

**Problem:** Error saying "[Errno 10048] Only one usage of each socket address is normally permitted"

**Solution:**
1. Find and kill the process using port 8000 or 3000
2. Or change the port in `main.py` (for backend) or `vite.config.js` (for frontend)

## 📊 Verifying Installation

1. Open http://localhost:3000
2. You should see the dashboard with:
   - Live video stream with bounding boxes
   - Real-time vehicle counts
   - Congestion index
   - FPS counter

If all these are working, congratulations! 🎉 Your Nepal Traffic Intelligence system is ready!
