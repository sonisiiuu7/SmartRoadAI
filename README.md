# 🚀 SmartRoadAI – Edge AI Road Monitoring System

SmartRoadAI is a real-time edge AI road monitoring system designed to detect potholes and road surface anomalies using computer vision on Raspberry Pi devices.

The system leverages a custom INT8-quantized object detection model running through Google AI Edge LiteRT for low-latency inference, enabling deployment on resource-constrained edge hardware. SmartRoadAI supports both live camera feeds and recorded road footage, making it suitable for road inspection, infrastructure monitoring, and smart-city applications.

---

## ✨ Features

### Real-Time Edge Inference

* Runs directly on Raspberry Pi hardware.
* Optimized using INT8 quantization for fast inference.
* Low-latency object detection using Google AI Edge LiteRT.

### Intelligent Road Monitoring

* Detects potholes in real time.
* Draws bounding boxes around detected road defects.
* Displays confidence scores and live FPS metrics.

### Multi-Source Input

* Live camera support through Picamera2.
* Video-file processing for offline testing and evaluation.

### Automated Event Logging

* Records detection events with timestamps.
* Stores confidence scores for later analysis.
* Cooldown mechanism prevents duplicate event spam.

### Lightweight Deployment

* Designed for Raspberry Pi 4 and Raspberry Pi 5.
* Works with modern Raspberry Pi OS releases.
* Suitable for edge AI and IoT deployments.

---

## 🏗 System Architecture

Road Camera Feed
→ Frame Acquisition (Picamera2 / Video Input)
→ Image Preprocessing
→ INT8 Quantized Detection Model
→ Pothole Detection
→ Event Logging
→ Real-Time Visualization

---

## 📂 Project Structure

```text
SmartRoadAI/
├── main.py
├── best-int8.tflite
├── requirements.txt
├── README.md
└── logs/
```

---

## 🛠 Technology Stack

* Python
* OpenCV
* NumPy
* Google AI Edge LiteRT
* TensorFlow Lite (INT8 Quantized Model)
* Raspberry Pi
* Picamera2

---

## 🚀 Running the Project

```bash
python main.py
```

Select one of the available modes:

### Live Camera Mode

Uses Raspberry Pi Camera Module through Picamera2.

### Video Analysis Mode

Processes recorded road footage for testing and evaluation.

---

## 📊 Example Output

Detection events are stored in:

```text
pothole_events.csv
```

Example:

```csv
Timestamp,Confidence
2026-02-18 14:30:05,0.85
2026-02-18 14:30:15,0.72
```

---

## 🔮 Future Improvements

* GPS-based pothole localization
* Road quality severity estimation
* Interactive monitoring dashboard
* Cloud-based analytics
* Smart-city integration
* Automated maintenance reporting

---

## 🎯 Applications

* Smart City Infrastructure
* Road Maintenance Monitoring
* Municipal Road Inspection
* Transportation Analytics
* Edge AI Research
* Intelligent Infrastructure Systems
