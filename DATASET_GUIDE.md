# Nepal Traffic Object Detection Dataset - Creation Guide

## Dataset Overview
A custom YOLO-formatted object detection dataset for Nepal's specific traffic conditions, prioritizing Kathmandu's roads, dense intersections, motorcycles, and microbuses!

## Classes
| Class ID | Class Name   | Description                                 |
|----------|--------------|---------------------------------------------|
| 0        | car          | Standard passenger cars, SUVs, hatchbacks  |
| 1        | motorcycle   | Motorbikes, scooters, two-wheelers         |
| 2        | bus          | Large public buses                           |
| 3        | truck        | Delivery trucks, lorries, cargo vehicles    |
| 4        | microbus     | Nepal-specific microbuses (Suzuki, etc.)   |

## Data Collection Priorities
### Location Priority
1. Kathmandu Valley (highest priority)
2. Major intersections: Durbar Marg, Putalisadak, Tripureshwor, Maitighar, Baneshwor
3. Ring Road sections
4. Other dense urban areas

### Scene Priority
1. Dense intersections (congested)
2. Motorcycle-heavy roads
3. Microbus-dominated routes
4. Mixed traffic scenarios
5. Morning/evening rush hours

### Condition Priority
1. Occluded vehicles (common in Nepal traffic)
2. Diverse lighting (daytime, dusk, low light, night if possible)
3. Moderate/heavy congestion
4. Roadside camera perspective (fixed, eye-level or elevated)

## Labeling Rules (YOLO Format)
### General Rules
- **Tight Bounding Boxes**: Fit boxes tightly around vehicles, minimal background
- **Full Coverage**: Box must include entire visible vehicle
- **Class Consistency**: Always use correct class ID/name (see table above)

### Specific Rules
- **Partially Visible Vehicles**: Label if ≥40% of vehicle is visible
- **Very Small/Unclear Objects**: Ignore distant, tiny, or completely unclear objects
- **Occlusions**: Label occluded vehicles (still count if ≥40% visible)
- **Motorcycles**: Label with rider(s) if they're on the motorcycle (box includes entire bike + riders)
- **Microbuses**: Make sure to distinguish microbuses from large buses!

### YOLO Format
Each labeled image needs a corresponding `.txt` file with the same name, with one line per object:
```
class_id x_center y_center width height
```
All values **normalized to 0-1** relative to image dimensions!

## Directory Structure
```
dataset/
├── raw_videos/          # Place your raw Nepal traffic MP4 videos here
├── extracted_frames/    # Frames extracted from raw videos (auto-generated)
├── labeled/             # Place your labeled images + YOLO txt here
├── train/               # Training split (auto-generated)
├── valid/               # Validation split (auto-generated)
├── test/                # Test split (auto-generated)
└── models/              # Trained models saved here (auto-generated)
```

## Data Collection Tools
- Use your smartphone/camera to record Kathmandu traffic
- Or collect public Nepal traffic videos (ensure copyright compliance!)
- Record in 1080p or higher for best results
- Record from a fixed position (like a roadside camera)
- Record rush hour scenes for dense traffic

## Labeling Tools
Recommended tools for labeling in YOLO format:
1. **LabelImg**: Free, open-source, supports YOLO format
2. **CVAT**: Open-source, web-based, good for collaboration
3. **Roboflow**: Web-based, easy to use, good for small datasets

## Post-Labeling Steps
After labeling your dataset:
1. Run the dataset stats script to verify class distribution
2. Split dataset (auto-handled by training pipeline)
3. Train your custom model!

## Quality Checks
Before training:
- At least 500 labeled images (minimum)
- Balanced class distribution (adjust if necessary)
- No labeling mistakes (wrong class, bad boxes)
- Tight, accurate bounding boxes
