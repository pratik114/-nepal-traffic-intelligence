import os
import shutil
import random
from pathlib import Path


def create_data_yaml(output_dir, class_names):
    data_yaml_content = f"""
path: {os.path.abspath(output_dir)}
train: train/images
val: valid/images
test: test/images

names:
"""
    for idx, name in enumerate(class_names):
        data_yaml_content += f"  {idx}: {name}\n"

    data_yaml_path = os.path.join(output_dir, "data.yaml")
    with open(data_yaml_path, "w") as f:
        f.write(data_yaml_content.strip())
    return data_yaml_path


def split_dataset(labeled_dir, output_dir, train_ratio=0.7, valid_ratio=0.2, test_ratio=0.1, seed=42):
    random.seed(seed)
    labeled_path = Path(labeled_dir)

    image_files = list(labeled_path.glob("*.jpg")) + list(labeled_path.glob("*.png"))
    random.shuffle(image_files)

    total = len(image_files)
    train_end = int(total * train_ratio)
    valid_end = train_end + int(total * valid_ratio)

    train_files = image_files[:train_end]
    valid_files = image_files[train_end:valid_end]
    test_files = image_files[valid_end:]

    for split_name, files in [("train", train_files), ("valid", valid_files), ("test", test_files)]:
        images_dir = os.path.join(output_dir, split_name, "images")
        labels_dir = os.path.join(output_dir, split_name, "labels")
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(labels_dir, exist_ok=True)

        for img_path in files:
            label_path = labeled_path / (img_path.stem + ".txt")
            shutil.copy(img_path, os.path.join(images_dir, img_path.name))
            if label_path.exists():
                shutil.copy(label_path, os.path.join(labels_dir, label_path.name))

    class_names = ["car", "motorcycle", "bus", "truck", "microbus"]
    data_yaml = create_data_yaml(output_dir, class_names)
    print(f"Dataset split complete! data.yaml created at: {data_yaml}")
    print(f"Train: {len(train_files)}, Valid: {len(valid_files)}, Test: {len(test_files)}")
    return data_yaml
