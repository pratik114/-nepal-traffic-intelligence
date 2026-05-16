import os
from pathlib import Path
from collections import defaultdict
import cv2


def verify_dataset(labeled_dir="dataset/labeled"):
    labeled_path = Path(labeled_dir)
    image_exts = [".jpg", ".jpeg", ".png"]
    class_names = ["car", "motorcycle", "bus", "truck", "microbus"]
    num_classes = len(class_names)

    image_files = []
    for ext in image_exts:
        image_files.extend(list(labeled_path.glob(f"*{ext}")))
    image_files = sorted(image_files)
    total_images = len(image_files)

    issues = []
    class_counts = defaultdict(int)
    label_file_matches = 0
    total_objects = 0

    print("=" * 80)
    print("NEPAL TRAFFIC DATASET - VERIFICATION REPORT")
    print("=" * 80)
    print(f"Dataset directory: {labeled_path.absolute()}")
    print(f"Total image files found: {total_images}")
    print("-" * 80)

    for img_file in image_files:
        label_file = labeled_path / (img_file.stem + ".txt")

        if not label_file.exists():
            issues.append(f"Missing label file for {img_file.name}")
            continue

        label_file_matches += 1

        try:
            img = cv2.imread(str(img_file))
            if img is None:
                issues.append(f"Could not read image {img_file.name}")
                continue
            img_h, img_w = img.shape[:2]
        except Exception as e:
            issues.append(f"Error reading {img_file.name}: {e}")
            continue

        try:
            with open(label_file, "r") as f:
                lines = [l.strip() for l in f.readlines() if l.strip()]

            for line_num, line in enumerate(lines, 1):
                parts = line.split()
                if len(parts) != 5:
                    issues.append(f"{label_file.name}:{line_num} - Invalid number of values (expected 5, got {len(parts)})")
                    continue

                try:
                    class_id = int(parts[0])
                    cx = float(parts[1])
                    cy = float(parts[2])
                    w = float(parts[3])
                    h = float(parts[4])
                except ValueError:
                    issues.append(f"{label_file.name}:{line_num} - Invalid numeric values")
                    continue

                if class_id < 0 or class_id >= num_classes:
                    issues.append(f"{label_file.name}:{line_num} - Invalid class ID {class_id} (must be 0-4)")
                    continue

                for coord, coord_name in [(cx, "cx"), (cy, "cy"), (w, "w"), (h, "h")]:
                    if coord < 0 or coord > 1:
                        issues.append(f"{label_file.name}:{line_num} - {coord_name} out of range (0-1): {coord}")

                class_counts[class_id] += 1
                total_objects += 1

        except Exception as e:
            issues.append(f"Error reading {label_file.name}: {e}")

    print("\nMATCHING REPORT:")
    print(f"Images with matching labels: {label_file_matches}/{total_images}")

    print("\nCLASS DISTRIBUTION:")
    print("-" * 40)
    for idx, name in enumerate(class_names):
        count = class_counts.get(idx, 0)
        percentage = (count / total_objects * 100) if total_objects > 0 else 0
        print(f"{name:12} (ID {idx}): {count:5} objects ({percentage:5.1f}%)")

    if issues:
        print("\nISSUES FOUND:")
        print("-" * 40)
        for issue in issues:
            print(f"• {issue}")
    else:
        print("\n[OK] NO ISSUES FOUND! Dataset is valid!")

    print("=" * 80)
    return {
        "total_images": total_images,
        "labeled_images": label_file_matches,
        "total_objects": total_objects,
        "class_counts": dict(class_counts),
        "issues": issues
    }


if __name__ == "__main__":
    verify_dataset()
