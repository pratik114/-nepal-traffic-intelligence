import os
import time
import threading
import cv2
import json
import numpy as np
from datetime import datetime
from backend.vision.detector import VehicleDetector
from backend.vision.tracker import VehicleTracker
from backend.vision.utils import (
    draw_bounding_box, draw_fps, draw_counts,
    draw_congestion, get_color_for_class, resize_frame,
    draw_alerts, blur_region
)
from backend.analytics.congestion import AnalyticsManager
from backend.analytics.alert_system import AlertSystem, DirectionalCounter
from backend.api.main import app, update_frame, update_analytics, get_current_video
import uvicorn


def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


def get_video_list(videos_dir="videos"):
    if not os.path.exists(videos_dir):
        return []
    video_files = []
    for file in os.listdir(videos_dir):
        if file.lower().endswith('.mp4'):
            video_files.append(file)
    return sorted(video_files)


def main():
    USE_CAMERA = False
    VIDEOS_DIR = "videos"
    DEFAULT_VIDEO = "input.mp4"
    OUTPUT_VIDEO = os.path.join("outputs", "output.mp4")
    HISTORY_FILE = os.path.join("outputs", "analytics_history.json")
    CONF_THRESHOLD = 0.1
    MAX_WIDTH = 1280

    video_list = get_video_list(VIDEOS_DIR)
    if not video_list:
        print("Error: No MP4 videos found in videos/ folder!")
        return

    current_video = DEFAULT_VIDEO if DEFAULT_VIDEO in video_list else video_list[0]

    def open_video(video_name):
        video_path = os.path.join(VIDEOS_DIR, video_name)
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video {video_path}")
            return None, None, None, None
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 30
        ret, first_frame = cap.read()
        if not ret or first_frame is None:
            print(f"Error: Could not read first frame of {video_name}")
            cap.release()
            return None, None, None, None
        frame = resize_frame(first_frame, MAX_WIDTH)
        out_height, out_width = frame.shape[:2]
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        return cap, fps, out_height, out_width

    cap, fps, out_height, out_width = open_video(current_video)
    if cap is None:
        return
    frame_area = out_width * out_width

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, fps, (out_width, out_height))

    detector = VehicleDetector(device="auto")
    tracker = VehicleTracker()
    analytics = AnalyticsManager()
    alert_system = AlertSystem()
    directional_counter = DirectionalCounter(line_y=out_height // 2)
    heatmap = None

    prev_time = 0
    analytics_history = []
    loop_count = 0
    
    confidence_history = []
    detection_history = []
    peak_vehicles = 0
    peak_time = None

    print("Starting FastAPI server in background...")
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    print("FastAPI server running at http://localhost:8000")
    print("Traffic live endpoint: http://localhost:8000/traffic/live")
    print("Traffic stream endpoint: http://localhost:8000/traffic/stream")
    print(f"Available videos: {', '.join(video_list)}")
    print(f"Processing video: {current_video}...")

    while True:
        # Check if video has been changed via API
        new_video = get_current_video()
        if new_video != current_video:
            print(f"🔄 Switching to video: {new_video}")
            cap.release()
            new_cap, new_fps, new_h, new_w = open_video(new_video)
            if new_cap is not None:
                current_video = new_video
                cap = new_cap
                fps = new_fps
                out_height = new_h
                out_width = new_w
                frame_area = out_width * out_width
                directional_counter = DirectionalCounter(line_y=out_height // 2)
                heatmap = None
                tracker = VehicleTracker()
                analytics = AnalyticsManager()
                print(f"✅ Switched to video: {current_video}")
            else:
                print(f"❌ Failed to switch to video: {new_video}")

        ret, frame = cap.read()
        if not ret:
            loop_count += 1
            print(f"🔁 Video restarted (loop #{loop_count})")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        frame = resize_frame(frame, MAX_WIDTH)

        if heatmap is None:
            heatmap = np.zeros((out_height, out_width), dtype=np.float32)

        detections, tracked_objects = detector.detect_and_track(frame, conf_threshold=CONF_THRESHOLD)
        tracker.update(tracked_objects)
        directional_counter.update(tracked_objects)

        face_boxes = detector.detect_faces(frame)
        for box in face_boxes:
            frame = blur_region(frame, box)

        for det in detections:
            color = get_color_for_class(det["class"])
            frame = draw_bounding_box(
                frame, det["bbox"], det["class"],
                det["confidence"], det.get("track_id"), color
            )

            x1, y1, x2, y2 = map(int, det["bbox"])
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            if 0 <= cy < heatmap.shape[0] and 0 <= cx < heatmap.shape[1]:
                heatmap[cy-10:cy+10, cx-10:cx+10] += 1

        current_time = time.time()
        fps_val = 1 / (current_time - prev_time) if (current_time - prev_time) > 0 else 0
        prev_time = current_time

        analytics.update(tracked_objects, fps_val, frame_area)
        analytics.total_count = tracker.get_total_count()
        analytics.class_counts = tracker.class_counts

        alerts = alert_system.update(
            analytics.congestion_index,
            analytics.traffic_status,
            tracked_objects
        )

        timestamp = datetime.now()
        directional_counts = directional_counter.get_counts()
        live_data = analytics.get_live_analytics(timestamp.isoformat())
        live_data["directional_counts"] = directional_counts
        live_data["alerts"] = alerts
        live_data["current_video"] = current_video

        avg_confidence = 0.0
        if detections:
            avg_confidence = sum(d["confidence"] for d in detections) / len(detections)
            confidence_history.append(avg_confidence)
            if len(confidence_history) > 100:
                confidence_history.pop(0)
            avg_confidence = sum(confidence_history) / len(confidence_history)

        current_frame_count = len(detections)
        detection_history.append({"time": timestamp, "count": current_frame_count})
        if len(detection_history) > 300:
            detection_history.pop(0)

        detection_rate = 0.0
        if len(detection_history) > 1:
            one_minute_ago = timestamp.timestamp() - 60
            recent_detections = [d for d in detection_history if d["time"].timestamp() > one_minute_ago]
            if recent_detections:
                detection_rate = sum(d["count"] for d in recent_detections)

        if current_frame_count > peak_vehicles:
            peak_vehicles = current_frame_count
            peak_time = timestamp.strftime("%H:%M")

        live_data["avg_confidence"] = avg_confidence
        live_data["current_frame_count"] = current_frame_count
        live_data["detection_rate"] = detection_rate
        live_data["peak_vehicles"] = peak_vehicles
        live_data["peak_time"] = peak_time

        update_analytics(live_data)

        analytics_history.append(live_data)
        if len(analytics_history) % 100 == 0:
            try:
                with open(HISTORY_FILE, "w") as f:
                    json.dump(analytics_history[-1000:], f)
            except Exception as e:
                print(f"Warning: Could not save history: {e}")

        frame = draw_fps(frame, fps_val)
        frame = draw_counts(frame, tracker.get_total_count(), tracker.get_class_counts())
        frame = draw_congestion(frame, analytics.congestion_index, analytics.traffic_status)
        frame = draw_alerts(frame, alerts)

        update_frame(frame)

        out.write(frame)

    cap.release()
    out.release()

    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(analytics_history, f)
        print(f"Analytics history saved to {HISTORY_FILE}")
    except Exception as e:
        print(f"Warning: Could not save final history: {e}")

    print(f"\nProcessing complete! Output saved to: {OUTPUT_VIDEO}")
    print(f"Total vehicles counted: {tracker.get_total_count()}")
    print(f"Per-class counts: {tracker.get_class_counts()}")
    print(f"Directional counts: {directional_counts}")


if __name__ == "__main__":
    import numpy as np
    main()
