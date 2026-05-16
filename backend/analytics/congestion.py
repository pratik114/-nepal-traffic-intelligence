from collections import defaultdict

def calculate_congestion(current_vehicle_count, frame_area, max_vehicle_density=0.0003):
    vehicle_density = current_vehicle_count / frame_area
    congestion_index = min(1.0, vehicle_density / max_vehicle_density)
    return congestion_index

def get_traffic_status(congestion_index):
    if congestion_index < 0.25:
        return "LOW"
    elif congestion_index < 0.5:
        return "MODERATE"
    elif congestion_index < 0.75:
        return "HEAVY"
    else:
        return "CRITICAL"

class AnalyticsManager:
    def __init__(self):
        self.total_count = 0
        self.class_counts = defaultdict(int)
        self.all_classes = ["car", "motorcycle", "bus", "truck", "microbus"]
        self.current_vehicles = 0
        self.congestion_index = 0.0
        self.traffic_status = "LOW"
        self.fps = 0.0

    def update(self, tracked_objects, fps, frame_area):
        self.current_vehicles = len(tracked_objects)
        self.congestion_index = calculate_congestion(self.current_vehicles, frame_area)
        self.traffic_status = get_traffic_status(self.congestion_index)
        self.fps = fps

    def update_counts(self, tracked_objects):
        current_ids = set(tracked_objects.keys())
        for obj_id, obj_data in tracked_objects.items():
            if obj_id not in self.class_counts:
                self.class_counts[obj_data["class"]] += 1
                self.total_count += 1

    def get_live_analytics(self, timestamp):
        per_class_full = {}
        for cls_name in self.all_classes:
            per_class_full[cls_name] = self.class_counts.get(cls_name, 0)
        return {
            "vehicle_counts": {
                "total": self.total_count,
                "per_class": per_class_full
            },
            "congestion_index": round(self.congestion_index, 2),
            "traffic_status": self.traffic_status,
            "fps": round(self.fps, 1),
            "timestamp": timestamp,
            "intersection": "Kathmandu Durbar Marg Intersection"
        }
