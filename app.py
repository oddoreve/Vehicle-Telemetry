import csv
import os
import time
from datetime import datetime
from flask import Flask, jsonify, render_template
baseDir = os.path.dirname(os.path.abspath(__file__))
csvPath = os.path.join(baseDir, "Telemetry.csv")
app = Flask(__name__)
def read_rows():
    if not os.path.exists(csvPath):
        return []
    with open(csvPath, newline="") as file:
        return list(csv.DictReader(file))
def convert_numbers(row):
    row["seq"] = int(row["seq"])
    for field in ("throttle", "speed", "rpm", "temp", "fuel",):
        row[field] = float(row[field])
    return row
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/api/latest")
def latest():
    rows = read_rows()
    if not rows:
        return jsonify({
            "online": False,
            "age_seconds": None,
            "data": None,
        })
    row = rows[-1]
    try:
        received_at = datetime.fromisoformat(row["timestamp"]).timestamp()
        age = max(0, time.time() - received_at)
    except (ValueError, TypeError, KeyError):
        age = float("inf")
    row = convert_numbers(row)
    return jsonify({
        "online": age < 5,
        "age_seconds": round(age, 1) if age != float("inf") else None,
        "data": row,
    })
@app.route("/api/history")
def history():
    rows = read_rows()[-120:]
    return jsonify([convert_numbers(row) for row in rows])
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
