from collections import defaultdict


class VehicleTracker:
    def __init__(self):
        self.counted_ids = set()
        self.class_counts = defaultdict(int)
        self.all_classes = ["car", "motorcycle", "bus", "truck", "microbus"]

    def update(self, tracked_objects):
        for track_id, obj_data in tracked_objects.items():
            if track_id not in self.counted_ids:
                self.counted_ids.add(track_id)
                class_name = obj_data["class"]
                self.class_counts[class_name] += 1

    def get_total_count(self):
        return len(self.counted_ids)

    def get_class_counts(self):
        full_counts = {}
        for cls_name in self.all_classes:
            full_counts[cls_name] = self.class_counts.get(cls_name, 0)
        return full_counts
