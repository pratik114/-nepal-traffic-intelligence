import os
from pathlib import Path
from collections import defaultdict


def analyze_dataset(labeled_dir="dataset/labeled"):
    labeled_path = Path(labeled_dir)
    image_files = list(labeled_path.glob("*.jpg")) + list(labeled_path.glob("*.png"))
    total_images = len(image_files)

    class_counts = defaultdict(int)
    class_names = ["car", "motorcycle", "bus", "truck", "microbus"]
    total_objects = 0

    for img_file in image_files:
        label_file = labeled_path / (img_file.stem + ".txt")
        if label_file.exists():
            with open(label_file, "r") as f:
                lines = [l.strip() for l in f.readlines() if l.strip()]
                for line in lines:
                    parts = line.split()
                    if parts:
                        class_id = int(parts[0])
                        if 0 <= class_id < len(class_names):
                            class_counts[class_id] += 1
                            total_objects += 1

    print("=" * 60)
    print("NEPAL TRAFFIC DATASET - STATISTICS")
    print("=" * 60)
    print(f"Total labeled images: {total_images}")
    print(f"Total labeled objects: {total_objects}")
    print("\nClass distribution:")
    print("-" * 40)
    for idx, name in enumerate(class_names):
        count = class_counts.get(idx, 0)
        percentage = (count / total_objects * 100) if total_objects > 0 else 0
        print(f"{name:12} (ID {idx}): {count:5} objects ({percentage:5.1f}%)")
    print("=" * 60)

    return {
        "total_images": total_images,
        "total_objects": total_objects,
        "class_counts": dict(class_counts),
        "class_names": class_names
    }


if __name__ == "__main__":
    analyze_dataset()
