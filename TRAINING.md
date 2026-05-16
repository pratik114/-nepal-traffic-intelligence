# 🧠 Training Guide

This guide will help you train your own custom YOLOv8 model for Nepal traffic detection.

## 📁 Dataset Preparation

### 1. Collect Images

- Capture images from Kathmandu intersections
- Include various lighting conditions (day, night, rainy)
- Cover multiple intersections
- Aim for at least 500-1000 images for good results

### 2. Annotate Images

#### Option A: Roboflow (Recommended)

1. Sign up for [Roboflow](https://roboflow.com/)
2. Create a new project
3. Upload your images
4. Annotate with these 5 classes:
   - `car`
   - `motorcycle`
   - `bus`
   - `truck`
   - `microbus`
5. Generate dataset version
6. Export in YOLOv8 format

#### Option B: Manual Labeling with LabelImg

1. Install LabelImg:
   ```bash
   pip install labelImg
   ```
2. Run LabelImg:
   ```bash
   labelImg
   ```
3. Set save format to YOLO
4. Annotate each image with bounding boxes
5. Save annotations in the same folder as images

### 3. Dataset Structure

Organize your dataset like this:
```
dataset/
├── train/
│   ├── images/
│   │   ├── image_001.jpg
│   │   └── image_002.jpg
│   └── labels/
│       ├── image_001.txt
│       └── image_002.txt
├── valid/
│   ├── images/
│   └── labels/
└── data.yaml
```

Create `data.yaml` with:
```yaml
path: ../dataset
train: train/images
val: valid/images

names:
  0: car
  1: motorcycle
  2: bus
  3: truck
  4: microbus
```

## 🚀 Training the Model

### 1. Configure Training

Edit `training/fine_tune_yolo.py` (or create it if needed):

```python
from ultralytics import YOLO

# Load pre-trained model
model = YOLO('yolov8n.pt')

# Train
results = model.train(
    data='dataset/data.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    device='cuda'  # or 'cpu' if no GPU
)

# Export to ONNX (optional)
model.export(format='onnx')
```

### 2. Run Training

```bash
python training/fine_tune_yolo.py
```

### 3. Expected Training Time

- **GPU (RTX 3060/4060)**: ~1-2 hours for 100 epochs
- **GPU (GTX 1650)**: ~3-4 hours for 100 epochs
- **CPU**: ~12-24 hours (not recommended)

### 4. GPU Memory Requirements

- **YOLOv8n**: 4GB VRAM minimum, 8GB recommended
- **YOLOv8s**: 6GB VRAM minimum, 12GB recommended
- **YOLOv8m**: 8GB VRAM minimum, 16GB recommended

## 📊 Monitoring Training

While training, you'll see:
- Loss values decreasing
- mAP (mean Average Precision) increasing
- Validation results after each epoch

Training outputs are saved in `runs/detect/train/`:
- `weights/best.pt` - Best model (use this!)
- `weights/last.pt` - Last epoch
- Plots: confusion matrix, PR curves, loss curves

## 🎯 Using Your Trained Model

### 1. Copy the Model

```bash
cp runs/detect/train/weights/best.pt models/nepal_traffic_best.pt
```

### 2. Update Detector (Optional)

Edit `backend/vision/detector.py` to use your custom model by default:

```python
# Change use_default to False
use_default = False
```

## 🔍 Evaluating Model Performance

Test your model:
```bash
python scripts/test_custom_model.py
```

Or use our test script:
```python
from ultralytics import YOLO
import cv2

model = YOLO('models/nepal_traffic_best.pt')
results = model('path/to/test/image.jpg')
results[0].show()
```

## 💡 Tips for Better Training

1. **More Data**: The more diverse images, the better
2. **Balanced Classes**: Try to have similar number of examples per class
3. **Quality Annotations**: Precise bounding boxes matter!
4. **Data Augmentation**: Roboflow does this automatically
5. **Train Longer**: Increase epochs if mAP is still improving

## ❓ Common Issues

### CUDA Out of Memory

**Solution:**
- Use smaller model (yolov8n instead of yolov8s)
- Reduce batch size
- Reduce image size (imgsz=416)

### Training Not Improving

**Solution:**
- Check dataset annotations
- Increase number of epochs
- Add more training data
- Adjust learning rate

### Model Not Detecting Well

**Solution:**
- Use best.pt, not last.pt
- Test on validation set
- Add more diverse training examples
- Check class distribution
