from flask import Flask, render_template
import json
import os

app = Flask(__name__)

@app.route("/")
def dashboard():
    # Load sensor data from cached JSON file
    with open("cached_data.json", "r") as f:
        sensors = json.load(f)
    return render_template("dashboard.html", sensors=sensors)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
