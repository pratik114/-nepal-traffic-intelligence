# Nepal Traffic Intelligence - Training Pipeline Guide

This guide will walk you through training a Nepal‑specific traffic detection model using your local videos!

## Directory Structure
```
dataset/
├── raw_videos/          # Place your raw traffic videos (.mp4) here
├── extracted_frames/    # Frames extracted from videos (auto-generated)
├── labeled/             # Place labeled images + YOLO .txt labels here
├── train/               # Train split (auto-generated)
├── valid/               # Validation split (auto-generated)
├── test/                # Test split (auto-generated)
└── models/              # Trained models saved here

training/
├── extract_frames.py    # Extract frames from raw videos
├── train.py             # Train custom YOLOv8 model
├── evaluate.py          # Evaluate trained model
└── utils.py             # Dataset utilities (split, data.yaml)
```

## Step 1: Prepare Raw Videos
Place your Nepal traffic videos (MP4 format) into `dataset/raw_videos/`.

## Step 2: Extract Frames
Run this to extract frames from your videos:
```powershell
.\venv\Scripts\Activate.ps1
python -m training.extract_frames
```

This will:
- Extract every 60th frame (configurable)
- Resize to 1280x720
- Save to `dataset/extracted_frames/`

## Step 3: Label Frames
Use a tool like **LabelImg**, **CVAT**, or **Roboflow** to label your frames in YOLO format:
- Create a `.txt` file for each image with the same name
- Each line: `class_id x_center y_center width height` (normalized 0–1)

Class IDs:
- 0: car
- 1: motorcycle
- 2: bus
- 3: truck
- 4: microbus

Place labeled images + `.txt` files into `dataset/labeled/`.

## Step 4: Train Model
```powershell
python -m training.train
```

This will:
- Split dataset 70% train / 20% valid / 10% test
- Generate `dataset/data.yaml`
- Train YOLOv8 (nano by default) on your custom dataset
- Save best/last weights to `dataset/models/nepal_traffic/weights/`

## Step 5: Evaluate Model
```powershell
python -m training.evaluate
```

This will:
- Evaluate on test set
- Generate confusion matrix
- Show precision, recall, mAP50, mAP50-95

## Step 6: Use Trained Model in Inference
The main inference system (`main.py`, `backend/vision/detector.py`) will **automatically** load the best trained model from `dataset/models/nepal_traffic/weights/best.pt` if it exists! No changes needed!

## Configuration Options
### extract_frames.py
Edit `training/extract_frames.py`:
- `every_nth_frame`: How often to extract frames
- `target_width`, `target_height`: Output frame size

### train.py
Edit `training/train.py`:
- `model_name`: Base model (yolov8n.pt, yolov8s.pt, etc.)
- `epochs`: Number of training epochs
- `batch_size`: Batch size (adjust for your GPU memory)
- `img_size`: Training image size
- `resume`: Resume training from last checkpoint

## Troubleshooting
- **CUDA out of memory**: Reduce `batch_size` or `img_size`
- **No labeled data**: Make sure your labeled images + txt files are in `dataset/labeled/`
- **Custom model not loading**: Verify `dataset/models/nepal_traffic/weights/best.pt` exists!
