import requests
import time

API_URL = "http://localhost:8000/traffic/live"

print("Testing /traffic/live endpoint...")
try:
    while True:
        try:
            response = requests.get(API_URL, timeout=2)
            if response.status_code == 200:
                data = response.json()
                print("\nAPI Response:")
                print(f"  Timestamp: {data.get('timestamp')}")
                print(f"  Total vehicles: {data.get('vehicle_counts', {}).get('total')}")
                print(f"  Per class: {data.get('vehicle_counts', {}).get('per_class')}")
                print(f"  Congestion: {data.get('congestion_index')}")
                print(f"  Status: {data.get('traffic_status')}")
                print(f"  FPS: {data.get('fps')}")
                print(f"  Alerts: {data.get('alerts')}")
            else:
                print(f"Error: {response.status_code}")
        except Exception as e:
            print(f"Request failed: {e}")
        time.sleep(2)
except KeyboardInterrupt:
    print("\nStopped.")
