from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
import cv2
import threading
import time
import numpy as np
import logging

# Setup logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Nepal Traffic Intelligence API")

# CORS configuration - allow everything for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# ============================================================
# THREAD-SAFE FRAME BUFFER (Critical for streaming)
# ============================================================
class FrameBuffer:
    def __init__(self):
        self._frame = None
        self._lock = threading.Lock()
        self._frame_count = 0
        self._last_update = time.time()
    
    def update(self, frame):
        """Called by video processor with new annotated frame"""
        if frame is None:
            return
        with self._lock:
            self._frame = frame.copy()
            self._frame_count += 1
            self._last_update = time.time()
    
    def get(self):
        """Called by stream endpoint to get latest frame"""
        with self._lock:
            if self._frame is None:
                return None
            return self._frame.copy()
    
    def stats(self):
        """Get buffer statistics"""
        with self._lock:
            return {
                "frame_count": self._frame_count,
                "last_update": self._last_update,
                "seconds_since_update": time.time() - self._last_update,
                "has_frame": self._frame is not None
            }

# Global instance
frame_buffer = FrameBuffer()
analytics_data = {
    "vehicle_counts": {"total": 0, "per_class": {}},
    "congestion_index": 0.0,
    "traffic_status": "LOW",
    "fps": 0.0,
    "alerts": []
}
analytics_lock = threading.Lock()

# ============================================================
# PLACEHOLDER FRAME (shown when video not ready)
# ============================================================
def create_placeholder_frame(message="Initializing..."):
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    frame[:] = (20, 20, 30)  # Dark blue-ish background
    
    cv2.putText(frame, "Nepal Traffic Intelligence",
                (80, 200), cv2.FONT_HERSHEY_SIMPLEX,
                0.9, (100, 200, 255), 2)
    cv2.putText(frame, message,
                (180, 260), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2)
    cv2.putText(frame, "Waiting for video processing...",
                (140, 320), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (150, 150, 150), 1)
    return frame

# ============================================================
# MJPEG STREAM GENERATOR (Bulletproof)
# ============================================================
def generate_mjpeg_stream():
    """
    Generator that yields MJPEG frames.
    Handles all edge cases: no frame, errors, slow updates.
    """
    logger.info("📹 New stream client connected")
    last_frame_time = time.time()
    frames_sent = 0
    
    try:
        while True:
            try:
                # Get latest frame
                frame = frame_buffer.get()
                
                # If no frame yet, send placeholder
                if frame is None:
                    frame = create_placeholder_frame("Connecting to camera...")
                
                # Encode as JPEG
                success, jpeg = cv2.imencode(
                    '.jpg', frame,
                    [cv2.IMWRITE_JPEG_QUALITY, 80]
                )
                
                if not success:
                    logger.warning("⚠️ JPEG encoding failed")
                    continue
                
                # Yield in MJPEG format
                yield (
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n'
                    b'Content-Length: ' + str(len(jpeg)).encode() + b'\r\n'
                    b'\r\n' + jpeg.tobytes() + b'\r\n'
                )
                
                frames_sent += 1
                
                # Log every 100 frames
                if frames_sent % 100 == 0:
                    logger.info(f"📤 Stream sent {frames_sent} frames")
                
                # Control frame rate (max 30 FPS)
                elapsed = time.time() - last_frame_time
                if elapsed < 0.033:  # 33ms = ~30 FPS
                    time.sleep(0.033 - elapsed)
                last_frame_time = time.time()
                
            except Exception as e:
                logger.error(f"❌ Stream error: {e}")
                time.sleep(0.1)
                continue
                
    except GeneratorExit:
        logger.info(f"👋 Stream client disconnected (sent {frames_sent} frames)")
    except Exception as e:
        logger.error(f"💥 Stream generator crashed: {e}")

# ============================================================
# API ENDPOINTS
# ============================================================

@app.get("/")
async def root():
    return {
        "service": "Nepal Traffic Intelligence",
        "status": "running",
        "endpoints": ["/health", "/traffic/live", "/traffic/stream"]
    }

@app.get("/health")
async def health():
    stats = frame_buffer.stats()
    return {
        "status": "healthy",
        "stream_active": stats["has_frame"],
        "frames_processed": stats["frame_count"],
        "last_frame_age_seconds": stats["seconds_since_update"]
    }

@app.get("/traffic/live")
async def live_analytics():
    with analytics_lock:
        return JSONResponse(content=analytics_data.copy())

@app.get("/traffic/stream")
async def video_stream():
    return StreamingResponse(
        generate_mjpeg_stream(),
        media_type="multipart/x-mixed-replace; boundary=frame",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
            "X-Accel-Buffering": "no"
        }
    )

# ============================================================
# UPDATE FUNCTIONS (called by video processor)
# ============================================================

def update_frame(frame):
    """Public function to update frame from video processor"""
    frame_buffer.update(frame)

def update_analytics(data):
    """Public function to update analytics from video processor"""
    global analytics_data
    with analytics_lock:
        analytics_data.update(data)
