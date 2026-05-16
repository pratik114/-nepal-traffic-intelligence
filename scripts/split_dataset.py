import os
import shutil
import random
from pathlib import Path
from collections import defaultdict


def split_dataset(
    labeled_dir="dataset/labeled",
    train_ratio=0.75,
    val_ratio=0.15,
    test_ratio=0.10,
    seed=42
):
    random.seed(seed)
    labeled_path = Path(labeled_dir)
    
    image_exts = [".jpg", ".jpeg", ".png"]
    class_names = ["car", "motorcycle", "bus", "truck", "microbus"]

    valid_pairs = []
    for img_path in labeled_path.iterdir():
        if img_path.suffix.lower() not in image_exts:
            continue
        label_path = labeled_path / (img_path.stem + ".txt")
        if label_path.exists():
            valid_pairs.append((img_path, label_path))

    if not valid_pairs:
        print("No valid image-label pairs found!")
        return

    random.shuffle(valid_pairs)
    total = len(valid_pairs)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)

    splits = {
        "train": valid_pairs[:train_end],
        "val": valid_pairs[train_end:val_end],
        "test": valid_pairs[val_end:]
    }

    split_class_counts = {
        "train": defaultdict(int),
        "val": defaultdict(int),
        "test": defaultdict(int)
    }

    for split_name, pairs in splits.items():
        split_images_dir = labeled_path / "images" / split_name
        split_labels_dir = labeled_path / "labels" / split_name
        split_images_dir.mkdir(parents=True, exist_ok=True)
        split_labels_dir.mkdir(parents=True, exist_ok=True)

        for img_path, label_path in pairs:
            shutil.copy(img_path, split_images_dir / img_path.name)
            shutil.copy(label_path, split_labels_dir / label_path.name)

            try:
                with open(label_path, "r") as f:
                    lines = [l.strip() for l in f.readlines() if l.strip()]
                for line in lines:
                    parts = line.split()
                    if parts:
                        class_id = int(parts[0])
                        if 0 <= class_id < len(class_names):
                            split_class_counts[split_name][class_id] += 1
            except Exception:
                pass

    yaml_content = f"""path: {labeled_path.absolute().as_posix()}
train: images/train
val: images/val
test: images/test

names:
  0: car
  1: motorcycle
  2: bus
  3: truck
  4: microbus
"""
    yaml_path = labeled_path / "dataset.yaml"
    with open(yaml_path, "w") as f:
        f.write(yaml_content)

    print("=" * 80)
    print("DATASET SPLIT COMPLETE")
    print("=" * 80)
    print(f"Total valid image-label pairs: {total}")
    print(f"Train:      {len(splits['train']):3} ({len(splits['train'])/total*100:.1f}%)")
    print(f"Validation: {len(splits['val']):3} ({len(splits['val'])/total*100:.1f}%)")
    print(f"Test:       {len(splits['test']):3} ({len(splits['test'])/total*100:.1f}%)")
    print("-" * 80)
    print("\nPER-SPLIT CLASS DISTRIBUTION")
    for split_name in ["train", "val", "test"]:
        print(f"\n{split_name.upper()}:")
        total_split = sum(split_class_counts[split_name].values())
        for idx, name in enumerate(class_names):
            cnt = split_class_counts[split_name].get(idx, 0)
            pct = (cnt / total_split * 100) if total_split > 0 else 0
            print(f"  {name:12}: {cnt:3} ({pct:5.1f}%)")
    print("\n" + "=" * 80)
    print(f"dataset.yaml created at: {yaml_path}")
    print("=" * 80)


if __name__ == "__main__":
    split_dataset()
