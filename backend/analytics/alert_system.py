from collections import defaultdict, deque
import time


class AlertSystem:
    def __init__(self):
        self.alerts = []
        self.congestion_history = deque(maxlen=30)
        self.vehicle_positions = defaultdict(lambda: deque(maxlen=10))

    def check_congestion(self, congestion_index, traffic_status):
        new_alerts = []
        if traffic_status == "CRITICAL":
            new_alerts.append({
                "type": "CRITICAL_CONGESTION",
                "message": "Critical congestion detected!",
                "timestamp": time.time()
            })
        elif traffic_status == "HEAVY":
            new_alerts.append({
                "type": "HEAVY_CONGESTION",
                "message": "Heavy congestion detected.",
                "timestamp": time.time()
            })
        return new_alerts

    def check_stalled_vehicles(self, tracked_objects):
        new_alerts = []
        for track_id, obj_data in tracked_objects.items():
            centroid = obj_data["centroid"]
            self.vehicle_positions[track_id].append(centroid)
            
            if len(self.vehicle_positions[track_id]) >= 10:
                positions = list(self.vehicle_positions[track_id])
                total_distance = 0
                for i in range(1, len(positions)):
                    dx = positions[i][0] - positions[i-1][0]
                    dy = positions[i][1] - positions[i-1][1]
                    total_distance += (dx**2 + dy**2)**0.5
                
                if total_distance < 50:
                    new_alerts.append({
                        "type": "STALLED_VEHICLE",
                        "message": f"Possible stalled vehicle (ID: {track_id})",
                        "track_id": track_id,
                        "timestamp": time.time()
                    })
        return new_alerts

    def update(self, congestion_index, traffic_status, tracked_objects):
        self.congestion_history.append(congestion_index)
        self.alerts = []
        
        self.alerts.extend(self.check_congestion(congestion_index, traffic_status))
        self.alerts.extend(self.check_stalled_vehicles(tracked_objects))
        
        return self.alerts


class DirectionalCounter:
    def __init__(self, line_y=None):
        self.line_y = line_y
        self.counts_entering = defaultdict(int)
        self.counts_leaving = defaultdict(int)
        self.vehicle_states = {}

    def set_line_y(self, line_y):
        self.line_y = line_y

    def update(self, tracked_objects):
        for track_id, obj_data in tracked_objects.items():
            centroid = obj_data["centroid"]
            class_name = obj_data["class"]
            
            if track_id not in self.vehicle_states:
                self.vehicle_states[track_id] = {"prev_y": centroid[1], "counted": False}
            else:
                prev_y = self.vehicle_states[track_id]["prev_y"]
                if self.line_y is not None and not self.vehicle_states[track_id]["counted"]:
                    if prev_y < self.line_y and centroid[1] >= self.line_y:
                        self.counts_entering[class_name] += 1
                        self.vehicle_states[track_id]["counted"] = True
                    elif prev_y > self.line_y and centroid[1] <= self.line_y:
                        self.counts_leaving[class_name] += 1
                        self.vehicle_states[track_id]["counted"] = True
                self.vehicle_states[track_id]["prev_y"] = centroid[1]

    def get_counts(self):
        return {
            "entering": dict(self.counts_entering),
            "leaving": dict(self.counts_leaving),
            "total_entering": sum(self.counts_entering.values()),
            "total_leaving": sum(self.counts_leaving.values())
        }
