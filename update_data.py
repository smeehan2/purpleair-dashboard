import pandas as pd
import requests
import json
import os
from datetime import datetime

# Load sensor data from CSV
df = pd.read_csv("cleaned_sensor_data.csv")

# Extract sensor indexes and read keys
sensor_info = df[["Sensor Index", "Sensor Read Key", "Sensor Name"]].dropna(subset=["Sensor Index"])
sensors = sensor_info.to_dict(orient="records")

# Collect all sensor indexes for batch request
sensor_indexes = [str(int(sensor["Sensor Index"])) for sensor in sensors]

# Prepare API request
API_KEY = "462A9FCB-1F5B-11EE-A77F-42010A800009"
url = "https://api.purpleair.com/v1/sensors"
headers = {"X-API-Key": API_KEY}
params = {
    "sensor_index": ",".join(sensor_indexes),
    "fields": "sensor_index,name,pm2.5,temperature,last_seen"
}

# Make the batch API request
try:
    response = requests.get(url, headers=headers, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()
    sensor_data_map = {entry["sensor_index"]: entry for entry in data.get("data", [])}
except Exception as e:
    print(f"Error fetching sensor data: {e}")
    sensor_data_map = {}

# Build the cached data structure
cached_data = []

for sensor in sensors:
    index = int(sensor["Sensor Index"])
    read_key = sensor.get("Sensor Read Key", "")
    name = sensor.get("Sensor Name", f"Sensor {index}")
    entry = sensor_data_map.get(index, {})

    # Fallback if batch data is missing or sensor is private
    if not entry:
        individual_url = f"https://api.purpleair.com/v1/sensors/{index}"
        individual_params = {}
        if pd.notna(read_key) and read_key != "":
            individual_params["read_key"] = read_key
        try:
            r = requests.get(individual_url, headers=headers, params=individual_params, timeout=10)
            if r.status_code == 200:
                entry = r.json().get("sensor", {})
        except Exception as e:
            print(f"Error fetching individual sensor {index}: {e}")

    # Parse data
    last_seen = entry.get("last_seen")
    pm25 = entry.get("pm2.5", "N/A")
    temp = entry.get("temperature", "N/A")
    online = False
    if last_seen:
        try:
            last_seen_dt = datetime.utcfromtimestamp(last_seen)
            online = (datetime.utcnow() - last_seen_dt).total_seconds() < 3600
        except:
            last_seen_dt = "N/A"
    else:
        last_seen_dt = "N/A"

    cached_data.append({
        "name": name,
        "index": index,
        "pm25": pm25,
        "temp": temp,
        "online": online,
        "last_seen": str(last_seen_dt)
    })

# Save to JSON file
with open("cached_data.json", "w") as f:
    json.dump(cached_data, f, indent=2)

print("Sensor data successfully cached to cached_data.json.")
