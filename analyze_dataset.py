
import os
from collections import defaultdict

def count_labels_in_dir(labels_dir):
    class_counts = defaultdict(int)
    if not os.path.exists(labels_dir):
        return class_counts
    for file in os.listdir(labels_dir):
        if file.endswith('.txt'):
            file_path = os.path.join(labels_dir, file)
            try:
                with open(file_path, 'r') as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) >= 1:
                            class_id = int(parts[0])
                            class_counts[class_id] += 1
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    return class_counts

def main():
    dataset_dir = os.path.join(os.getcwd(), "dataset", "labeled")
    train_labels_dir = os.path.join(dataset_dir, "train", "labels")
    valid_labels_dir = os.path.join(dataset_dir, "valid", "labels")
    test_labels_dir = os.path.join(dataset_dir, "test", "labels")
    
    data_yaml_path = os.path.join(dataset_dir, "data.yaml")
    class_names = []
    if os.path.exists(data_yaml_path):
        import yaml
        with open(data_yaml_path, 'r') as f:
            data = yaml.safe_load(f)
            class_names = data.get('names', [])
    
    print("=" * 60)
    print("DATASET ANALYSIS")
    print("=" * 60)
    
    total_counts = defaultdict(int)
    
    splits = [
        ("Train", train_labels_dir),
        ("Valid", valid_labels_dir),
        ("Test", test_labels_dir)
    ]
    
    for split_name, labels_dir in splits:
        counts = count_labels_in_dir(labels_dir)
        print(f"\n{split_name} Set:")
        if not counts:
            print("  No labels found")
            continue
        
        total_in_split = sum(counts.values())
        print(f"  Total objects: {total_in_split}")
        
        for class_id in sorted(counts.keys()):
            count = counts[class_id]
            name = class_names[class_id] if class_id < len(class_names) else f"Class {class_id}"
            print(f"  - {name}: {count}")
            total_counts[class_id] += count
    
    print("\n" + "=" * 60)
    print("TOTAL DATASET:")
    print("=" * 60)
    for class_id in sorted(total_counts.keys()):
        count = total_counts[class_id]
        name = class_names[class_id] if class_id < len(class_names) else f"Class {class_id}"
        print(f"  - {name}: {count}")
    
    print("\n" + "=" * 60)
    print("TRAINING METRICS (from runs/detect/train/results.csv)")
    print("=" * 60)
    
    results_csv = os.path.join(os.getcwd(), "runs", "detect", "train", "results.csv")
    if os.path.exists(results_csv):
        import pandas as pd
        df = pd.read_csv(results_csv)
        last_epoch = df.iloc[-1]
        print(f"Final Epoch: {int(last_epoch['epoch'])}")
        print(f"mAP@0.5: {last_epoch['metrics/mAP50(B)']:.4f}")
        print(f"mAP@0.5:0.95: {last_epoch['metrics/mAP50-95(B)']:.4f}")
        print(f"Precision: {last_epoch['metrics/precision(B)']:.4f}")
        print(f"Recall: {last_epoch['metrics/recall(B)']:.4f}")

if __name__ == "__main__":
    main()
