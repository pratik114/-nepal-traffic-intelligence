import cv2
import numpy as np


def draw_bounding_box(frame, box, class_name, confidence, track_id=None, color=(0, 255, 0)):
    x1, y1, x2, y2 = map(int, box)
    label = f"{class_name} {confidence:.2f}"
    
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    
    label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
    
    overlay = frame.copy()
    cv2.rectangle(overlay, (x1, y1 - label_size[1] - 8),
                  (x1 + label_size[0] + 10, y1), color, -1)
    cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
    
    cv2.putText(frame, label, (x1 + 5, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    
    return frame


def draw_fps(frame, fps):
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    return frame


def draw_counts(frame, total_count, class_counts):
    y_offset = 70
    cv2.putText(frame, f"Total Vehicles: {total_count}", (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    y_offset += 30
    for class_name, count in class_counts.items():
        cv2.putText(frame, f"{class_name}: {count}", (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        y_offset += 25
    return frame


def draw_congestion(frame, congestion_index, traffic_status):
    y_offset = 200
    status_colors = {
        "LOW": (0, 255, 0),
        "MODERATE": (0, 255, 255),
        "HEAVY": (0, 165, 255),
        "CRITICAL": (0, 0, 255)
    }
    color = status_colors.get(traffic_status, (255, 255, 255))
    cv2.putText(frame, f"Congestion: {congestion_index:.2f}", (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    y_offset += 30
    cv2.putText(frame, f"Status: {traffic_status}", (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    return frame


def get_color_for_class(class_name):
    colors = {
        "car": (16, 185, 129),
        "motorcycle": (249, 115, 22),
        "bus": (59, 130, 246),
        "truck": (239, 68, 68),
        "microbus": (168, 85, 247)
    }
    return colors.get(class_name, (255, 255, 255))


def resize_frame(frame, max_width=1280):
    height, width = frame.shape[:2]
    if width > max_width:
        scale = max_width / width
        new_width = max_width
        new_height = int(height * scale)
        return cv2.resize(frame, (new_width, new_height))
    return frame


def blur_region(frame, box, kernel_size=25):
    x1, y1, x2, y2 = map(int, box)
    if x1 < 0 or y1 < 0 or x2 > frame.shape[1] or y2 > frame.shape[0]:
        return frame
    roi = frame[y1:y2, x1:x2]
    blurred = cv2.GaussianBlur(roi, (kernel_size, kernel_size), 30)
    frame[y1:y2, x1:x2] = blurred
    return frame


def draw_heatmap(frame, heatmap, alpha=0.5):
    heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    return cv2.addWeighted(frame, 1 - alpha, heatmap_colored, alpha, 0)


def draw_alerts(frame, alerts):
    y_offset = 300
    for alert in alerts:
        alert_colors = {
            "HEAVY_CONGESTION": (0, 165, 255),
            "CRITICAL_CONGESTION": (0, 0, 255),
            "STALLED_VEHICLE": (255, 165, 0),
            "ACCIDENT": (0, 0, 255)
        }
        color = alert_colors.get(alert["type"], (255, 255, 255))
        cv2.putText(frame, f"ALERT: {alert['message']}", (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        y_offset += 30
    return frame

