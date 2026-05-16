# 🚦 Nepal Traffic Intelligence

> AI-powered real-time traffic monitoring for Kathmandu

![Status](https://img.shields.io/badge/status-MVP_Complete-brightgreen)
![Tech](https://img.shields.io/badge/tech-YOLOv8%20%7C%20FastAPI%20%7C%20React-blue)

## 🚨 Problem Statement

Kathmandu faces severe traffic congestion crises:
- No real-time traffic monitoring infrastructure
- Manual vehicle counting is inefficient and error-prone
- Lack of data-driven congestion management
- No early warning system for traffic jams

## 💡 Solution

Nepal Traffic Intelligence is an AI-powered system that provides:
- Real-time vehicle detection and tracking
- Multi-class vehicle classification (5 types including microbus)
- Live congestion scoring and analytics
- Beautiful, intuitive dashboard for monitoring

## ✨ Key Features

- ✅ Real-time vehicle detection and tracking
- ✅ 5 vehicle classes: car, motorcycle, bus, truck, microbus
- ✅ Custom YOLOv8 model trained on Nepal traffic data
- ✅ Live MJPEG video streaming with bounding boxes
- ✅ ByteTrack for multi-object tracking with unique IDs
- ✅ Real-time congestion index calculation
- ✅ Stalled vehicle alerts
- ✅ Beautiful React + Tailwind dashboard
- ✅ GPU acceleration (CUDA support)
- ✅ Face blur for privacy protection

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| AI Model | YOLOv8 (custom-trained) |
| Tracking | ByteTrack |
| Backend | FastAPI (Python 3.13) |
| Frontend | React + Vite + Tailwind CSS |
| Visualization | Recharts |
| GPU | CUDA / NVIDIA |

## 📸 Screenshots

> **Note:** Add screenshots to `docs/` folder!

![Dashboard](docs/dashboard.png)
*Main dashboard showing real-time traffic analytics*

![Detection](docs/detection.png)
*Vehicle detection with bounding boxes and tracking*

## 🚀 Quick Start

For detailed installation instructions, see [setup.md](setup.md).

### Prerequisites
- Python 3.13+
- Node.js 18+
- NVIDIA GPU (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/pratik114/nepal-traffic-intelligence.git
   cd nepal-traffic-intelligence
   ```

2. **Backend Setup**
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows
   # source venv/bin/activate  # Linux/macOS
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Run the System**
   ```bash
   # Terminal 1 - Backend
   python main.py
   
   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

5. **Open Dashboard**
   Visit: http://localhost:3000

## 📁 Project Structure

```
nepal-traffic-intelligence/
├── backend/
│   ├── api/
│   │   └── main.py          # FastAPI endpoints
│   ├── analytics/
│   │   ├── storage.py        # Analytics database
│   │   ├── congestion.py     # Congestion calculation
│   │   └── alert_system.py   # Alert generation
│   └── vision/
│       ├── detector.py       # Vehicle detection
│       ├── tracker.py        # Object tracking
│       └── utils.py          # Drawing and helper functions
├── frontend/
│   └── src/
│       └── App.jsx           # Main dashboard component
├── models/                   # Trained models (not in repo)
├── videos/                   # Input videos (not in repo)
├── outputs/                  # Processed outputs (not in repo)
├── main.py                   # Main entry point
└── requirements.txt
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/traffic/live` | GET | Real-time traffic analytics |
| `/traffic/stream` | GET | MJPEG video stream |
| `/traffic/history` | GET | Historical analytics data |
| `/traffic/videos` | GET | List available videos |
| `/traffic/change-video` | POST | Change input video |

## 🧠 Custom Model Training

For detailed training instructions, see [TRAINING.md](TRAINING.md).

1. **Prepare Dataset**
   - Use Roboflow for annotation
   - Label 5 classes: car, motorcycle, bus, truck, microbus

2. **Train Model**
   ```bash
   python training/fine_tune_yolo.py
   ```

3. **Use Trained Model**
   Place model in `models/nepal_traffic_best.pt`

## 🗺️ Roadmap

- ✅ **Phase 1**: Basic vehicle detection
- ✅ **Phase 2**: Tracking and analytics
- ✅ **Phase 3**: Dashboard (MVP Complete)
- 🔜 **Phase 4**: Pilot deployment
- 🔜 **Phase 5**: Multi-intersection monitoring
- 🔜 **Phase 6**: Mobile app integration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

- **Author**: Pratik
- **GitHub**: [@pratik114](https://github.com/pratik114)

---

Made with ❤️ for Kathmandu's traffic management!
