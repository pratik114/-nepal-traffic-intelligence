import sqlite3
import os
from datetime import datetime


class AnalyticsStorage:
    def __init__(self, db_path="outputs/analytics.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                total_vehicles INTEGER NOT NULL,
                car_count INTEGER DEFAULT 0,
                motorcycle_count INTEGER DEFAULT 0,
                bus_count INTEGER DEFAULT 0,
                truck_count INTEGER DEFAULT 0,
                microbus_count INTEGER DEFAULT 0,
                congestion_index REAL NOT NULL,
                traffic_status TEXT NOT NULL,
                fps REAL
            )
        """)
        conn.commit()
        conn.close()

    def insert(self, data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        per_class = data["vehicle_counts"]["per_class"]
        cursor.execute("""
            INSERT INTO analytics (
                timestamp, total_vehicles, car_count, motorcycle_count,
                bus_count, truck_count, microbus_count, congestion_index,
                traffic_status, fps
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["timestamp"],
            data["vehicle_counts"]["total"],
            per_class.get("car", 0),
            per_class.get("motorcycle", 0),
            per_class.get("bus", 0),
            per_class.get("truck", 0),
            per_class.get("microbus", 0),
            data["congestion_index"],
            data["traffic_status"],
            data.get("fps")
        ))
        conn.commit()
        conn.close()

    def get_history(self, limit=100):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, timestamp, total_vehicles, car_count, motorcycle_count,
                   bus_count, truck_count, microbus_count, congestion_index,
                   traffic_status, fps
            FROM analytics
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            history.append({
                "id": row[0],
                "timestamp": row[1],
                "vehicle_counts": {
                    "total": row[2],
                    "per_class": {
                        "car": row[3],
                        "motorcycle": row[4],
                        "bus": row[5],
                        "truck": row[6],
                        "microbus": row[7]
                    }
                },
                "congestion_index": row[8],
                "traffic_status": row[9],
                "fps": row[10]
            })
        return list(reversed(history))
