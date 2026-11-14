import csv
import json
import os
import time
from datetime import datetime, timezone
import serial
from serial.tools import list_ports
baseDir = os.path.dirname(os.path.abspath(__file__))
csvPath = os.path.join(baseDir, "Telemetry.csv")
rate = 115200
arduinoPort = "/dev/ttyACM0"
fields = ["timestamp", "seq", "throttle", "speed", "rpm", "temp", "fuel",]
def validate(data):
    required = ["seq", "throttle", "speed", "rpm", "temp", "fuel",]
    for key in required:
        if key not in data:
            raise ValueError(f"Missing field: {key}")
    row = {
        "seq": int(data["seq"]),
        "throttle": float(data["throttle"]),
        "speed": float(data["speed"]),
        "rpm": float(data["rpm"]),
        "temp": float(data["temp"]),
        "fuel": float(data["fuel"]),
    }
    return row
def initialize_csv():
    if not os.path.exists(csvPath) or os.path.getsize(csvPath) == 0:
        with open(csvPath, "w", newline = "") as file:
            writer = csv.DictWriter(file, fieldnames = fields)
            writer.writeheader()
def main():
    initialize_csv()
    print(f"Connecting to {arduinoPort} at {rate} baud")
    print(f"Appending telemetry to {csvPath}")
    with serial.Serial(arduinoPort, rate, timeout = 2) as ser:
        time.sleep(2)
        ser.reset_input_buffer()
        with open(csvPath, "a", newline = "", buffering = 1) as file:
            writer = csv.DictWriter(file, fieldnames = fields)
            while True:
                try:
                    line = ser.readline().decode("utf-8", errors="replace").strip()
                    if not line:
                        continue
                    data = json.loads(line)
                    row = validate(data)
                    row["timestamp"] = datetime.now(timezone.utc).isoformat()
                    writer.writerow(row)
                    file.flush()
                    print(
                        f"seq={row['seq']} "
                        f"speed={row['speed']:.1f} km/h "
                        f"rpm={row['rpm']:.0f} "
                        f"temp={row['temp']:.1f} C"
                    )
                except (json.JSONDecodeError, ValueError, TypeError) as exc:
                    print(f"Skipping invalid record: {exc}")
                except KeyboardInterrupt:
                    print("\nCollector stopped.")
                    break
if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, serial.SerialException, OSError) as exc:
        print(f"Collector error: {exc}")
        raise SystemExit(1)