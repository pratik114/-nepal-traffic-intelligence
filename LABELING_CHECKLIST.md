# Nepal Traffic Dataset - Labeling Checklist

Use this checklist to ensure high-quality, consistent labels!

## Before You Start
- [ ] Read DATASET_GUIDE.md completely
- [ ] Understand all 5 classes (car/motorcycle/bus/truck/microbus)
- [ ] Know the difference between microbus and large bus!
- [ ] Set up your labeling tool for YOLO format

## Per-Image Checklist
For **every image** you label:
- [ ] Label all ≥40% visible vehicles
- [ ] Ignore tiny/unclear distant vehicles
- [ ] Use tight bounding boxes (minimal background)
- [ ] Boxes include entire visible vehicle
- [ ] No partial boxes cut off vehicles unnecessarily
- [ ] Correct class ID assigned to every object
- [ ] No objects missed in dense traffic
- [ ] No duplicate labels on same object
- [ ] Label occluded vehicles if ≥40% visible
- [ ] Label motorcycles with riders (box entire bike)
- [ ] Microbuses labeled correctly (not as bus/car)

## Per-Class Reminders
- **Car (0)**: Passenger cars, SUVs, hatchbacks, sedans
- **Motorcycle (1)**: Motorbikes, scooters, any two-wheeler
- **Bus (2)**: Large full-size buses only
- **Truck (3)**: Delivery trucks, lorries, cargo vehicles
- **Microbus (4)**: Small Nepal-specific microbuses!

## Final Check Before Training
- [ ] ≥500 labeled images total
- [ ] Balanced class distribution (adjust if needed)
- [ ] No obvious labeling errors
- [ ] All labeled images have corresponding .txt file
- [ ] YOLO format correct (normalized coordinates 0-1)
- [ ] Class IDs 0-4 only, no other numbers!
