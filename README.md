# Vehicle Telemetry Monitoring System

An Arduino Uno and Raspberry Pi 4 based vehicle telemetry monitoring system that collects, processes, stores, and visualizes vehicle-related data through a live web dashboard.

## Project Overview

This project demonstrates a basic vehicle telemetry system using an Arduino Uno for data acquisition and a Raspberry Pi 4 for data processing, storage, and visualization.

The Arduino reads throttle input from a potentiometer and temperature from an LM35 sensor. Vehicle speed, RPM, and fuel level are simulated using programmed logic.

The Raspberry Pi receives telemetry data through USB serial communication, stores timestamped records in a CSV file, and displays the information through a Flask-based web dashboard.

## Features

- Real-time throttle input monitoring
- Simulated vehicle speed (0–220 km/h)
- Simulated engine RPM (up to 6000 RPM)
- Temperature monitoring using LM35
- Simulated fuel consumption
- Serial communication between Arduino and Raspberry Pi
- Timestamped telemetry data collection
- Permanent CSV data storage
- Web-based dashboard using Flask
- Telemetry visualization using charts

## Hardware Components

| Component | Purpose |
|---|---|
| Arduino Uno | Sensor data acquisition and simulation |
| Raspberry Pi 4 | Data processing, storage and web server |
| 10k Potentiometer | Throttle input simulation |
| LM35 Temperature Sensor | Temperature measurement |
| USB Cable | Arduino-to-Raspberry Pi communication |
| Jumper Wires | Circuit connections |

## Software and Technologies

- Python
- Arduino C/C++
- Flask
- PySerial
- HTML
- CSS
- JavaScript
- Chart.js
- CSV
- Git and GitHub

## System Architecture

```text
       10k Potentiometer
              |
              v
          Arduino Uno
              ^
              |
          LM35 Sensor
              |
              v
     USB Serial Communication
              |
              v
        Raspberry Pi 4
              |
              v
         collector.py
              |
              v
        Telemetry.csv
              |
              v
            app.py
              |
              v
        Flask Web Server
              |
              v
        HTML Dashboard
              |
              v
       Telemetry Visualization
```

## Circuit Connections

### Potentiometer

| Potentiometer Pin | Arduino Uno |
|---|---|
| First outer pin | 5V |
| Middle pin | A0 |
| Other outer pin | GND |

### LM35 Temperature Sensor

With the flat face of the LM35 facing you and its legs pointing downward:

| LM35 Pin | Arduino Uno |
|---|---|
| Left pin (+Vs) | 5V |
| Middle pin (Vout) | A4 |
| Right pin (GND) | GND |

## Data Collection

The Arduino sends telemetry records in JSON format over USB serial communication at 115200 baud.

The Python collector:

1. Reads incoming serial data.
2. Parses JSON records.
3. Validates incoming values.
4. Adds a UTC timestamp.
5. Stores records in `Telemetry.csv`.

JSON is used only for serial data transmission. CSV is used for permanent data storage.

### CSV Data Format

```csv
timestamp,seq,throttle_pct,speed_kmh,rpm,ambient_temp_c,fuel_pct
```

## Project Structure

```text
TelemetrySystem/
│
├── collector.py
├── app.py
├── README.md
├── .gitignore
│
└── templates/
    └── index.html
```

`Telemetry.csv` is generated automatically when the collector runs and is excluded from Git tracking.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Vehicle-Telemetry-System.git
```

### 2. Navigate to the Project Folder

```bash
cd Vehicle-Telemetry-System
```

### 3. Install Dependencies

On Raspberry Pi OS:

```bash
sudo apt update
sudo apt install python3-flask python3-serial -y
```

### 4. Upload Arduino Code

- Open the Arduino IDE.
- Connect the Arduino Uno.
- Upload the Arduino program.
- Connect the Arduino to the Raspberry Pi through USB.

### 5. Run the Data Collector

```bash
python3 collector.py
```

### 6. Start the Flask Dashboard

Open a second terminal:

```bash
python3 app.py
```

### 7. Open the Dashboard

Open a browser and visit:

```text
http://127.0.0.1:5000
```

## Data Simulation Details

| Parameter | Implementation |
|---|---|
| Throttle | Read from potentiometer |
| Speed | Simulated based on throttle input |
| RPM | Simulated based on vehicle speed |
| Temperature | Measured using LM35 |
| Fuel | Simulated gradual decrease |

**Note:** This is a prototype and simulation-based telemetry project. Speed, RPM and fuel are not measured using actual vehicle sensors. The temperature sensor measures its local surroundings and is not connected to an actual engine.

## Future Improvements

- Add GPS-based vehicle location tracking.
- Integrate actual speed and RPM sensors.
- Implement engine diagnostics.
- Add historical telemetry analysis.
- Introduce data export and reporting.
- Improve dashboard responsiveness and visualization.
- Add alerts for abnormal sensor readings.

## Learning Outcomes

Through this project, I explored:

- Arduino sensor interfacing and analog data acquisition.
- Serial communication between microcontrollers and Raspberry Pi.
- Python-based data collection and validation.
- CSV data logging and timestamp management.
- Flask web application development.
- Real-time telemetry visualization.
- Integration of hardware and software components.

## Author

**Ananya Rayate**

GitHub: https://github.com/oddoreve

---

*Developed as an embedded systems and IoT learning project using Arduino Uno and Raspberry Pi 4.*
