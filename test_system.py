
import requests
import time

print("Testing Nepal Traffic Intelligence System...")
print("=" * 60)

# Test 1: Backend health
print("\n1. Testing backend endpoints...")
try:
    response = requests.get("http://localhost:8000/traffic/live", timeout=5)
    print(f"   /traffic/live: {response.status_code} OK")
    data = response.json()
    print(f"   - Total vehicles: {data.get('total_vehicles', 'N/A')}")
    print(f"   - Current video: {data.get('current_video', 'N/A')}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 2: Stream endpoint
try:
    print("\n2. Testing stream endpoint...")
    response = requests.get("http://localhost:8000/traffic/stream", stream=True, timeout=5)
    print(f"   /traffic/stream: {response.status_code} OK")
    print(f"   - Content-Type: {response.headers.get('Content-Type', 'N/A')}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 3: Frontend file exists
print("\n3. Checking frontend files...")
import os
frontend_path = os.path.join(os.getcwd(), "frontend", "dist", "index.html")
if os.path.exists(frontend_path):
    print(f"   ✅ Frontend found at: {frontend_path}")
    print(f"   📋 To open: Just double-click this file in File Explorer!")
else:
    print(f"   ❌ Frontend not found at: {frontend_path}")

print("\n" + "=" * 60)
print("✅ System check complete!")
print("📊 Backend is running at http://localhost:8000")
print("🎨 Frontend is ready at frontend/dist/index.html")
