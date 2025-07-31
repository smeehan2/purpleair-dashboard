from flask import Flask, render_template
import pandas as pd
import requests
import datetime

app = Flask(__name__)

def fetch_sensor_data(sensor_index, read_key):
    url = f"https://api.purpleair.com/v1/sensors/{sensor_index}"
    headers = {"X-API-Key": "YOUR_API_KEY_HERE"}  # Replace with your actual PurpleAir API key
    params = {}

    if pd.notna(read_key) and read_key != "":
        params["read_key"] = read_key  # Add read_key as a query parameter

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        print(f"Sensor {sensor_index} response status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()["sensor"]
            last_seen = datetime.datetime.utcfromtimestamp(data["last_seen"])
            pm25 = data.get("pm2.5", "N/A")
            temp = data.get("temperature", "N/A")
            online = (datetime.datetime.utcnow() - last_seen).total_seconds() < 3600
            print(f"Sensor {sensor_index} last seen: {last_seen}, online: {online}")
            return {"pm25": pm25, "temp": temp, "online": online, "last_seen": last_seen}
    except Exception as e:
        print(f"Error fetching sensor {sensor_index}: {e}")

    return {"pm25": "N/A", "temp": "N/A", "online": False, "last_seen": "N/A"}

@app.route("/")
def dashboard():
    df = pd.read_csv("cleaned_sensor_data.csv")
    sensors = []
    for _, row in df.iterrows():
        data = fetch_sensor_data(row["Sensor Index"], row["Sensor Read Key"])
        sensors.append({
            "name": row["Sensor Name"],
            "index": row["Sensor Index"],
            "pm25": data["pm25"],
            "temp": data["temp"],
            "online": data["online"],
            "last_seen": data["last_seen"]
        })
    return render_template("dashboard.html", sensors=sensors)

import os

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
