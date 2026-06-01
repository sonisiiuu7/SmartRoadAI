# 🚀 SmartRoadAI

### Real-Time Edge AI Road Monitoring Platform

SmartRoadAI is an Edge AI-powered road monitoring platform designed to detect potholes and road surface anomalies in real time.

The project combines computer vision, edge inference, event logging, and a cloud-hosted analytics dashboard to demonstrate how AI can be used for intelligent infrastructure monitoring.

---

# 🌐 Live Demo

### Dashboard

https://smartroadai-qdln.onrender.com

---

# 🎯 Project Overview

Road infrastructure monitoring is often performed manually, making it difficult to identify road defects efficiently and at scale.

SmartRoadAI addresses this challenge through:

* AI-based pothole detection
* Edge-device compatible architecture
* Automated event logging
* Historical analytics
* Cloud-hosted monitoring dashboard

The system is designed for deployment on Raspberry Pi-compatible edge devices while providing centralized monitoring through a web-based dashboard.

---

# ✨ Features

## Edge AI Detection

* Real-time pothole detection
* TensorFlow Lite based inference
* Google AI Edge LiteRT integration
* INT8 quantized model support
* Edge-device compatible architecture

## Analytics Dashboard

* Live monitoring interface
* Detection statistics
* Average confidence metrics
* Historical detection logs
* Weekly activity visualization
* Responsive dark-themed UI

## Event Monitoring

* Timestamped event logging
* Confidence score tracking
* Historical analytics
* Automatic dashboard refresh

## Cloud Deployment

* Flask-based web dashboard
* Hosted on Render
* Public monitoring portal
* GitHub-integrated deployment workflow

---

# 🏗 System Architecture

```text
┌─────────────────────────────────┐
│ Edge Device                     │
│ (Raspberry Pi Compatible)       │
│                                 │
│ Camera Input                    │
│        │                        │
│        ▼                        │
│ AI Detection Pipeline           │
│        │                        │
│        ▼                        │
│ Pothole Detection Events        │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│ Event Log Storage              │
│                                 │
│ smartroad_events.csv           │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│ Flask Analytics Dashboard      │
│                                 │
│ Total Detections               │
│ Confidence Analytics           │
│ Historical Records             │
│ Activity Monitoring            │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│ Cloud Deployment (Render)      │
│                                 │
│ Public Monitoring Portal       │
└─────────────────────────────────┘
```

---

# 🛠 Technology Stack

## AI & Computer Vision

* Python
* OpenCV
* NumPy
* TensorFlow Lite
* Google AI Edge LiteRT

## Edge Computing

* Raspberry Pi Compatible Architecture
* Picamera2 Support

## Backend

* Flask

## Deployment

* Render
* GitHub

---

# 📂 Project Structure

```text
SmartRoadAI
│
├── main.py
├── dashboard.py
├── best-int8.tflite
├── smartroad_events.csv
├── dashboard_preview.png
├── requirements.txt
├── requirements-web.txt
├── README.md
│
└── .gitignore
```

---

# 🚀 Local Setup

## Clone Repository

```bash
git clone https://github.com/sonisiiuu7/SmartRoadAI.git
cd SmartRoadAI
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Dashboard

```bash
python dashboard.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# 📊 Dashboard Metrics

The dashboard provides:

* Total detections
* Average confidence score
* Latest detection information
* Historical event logs
* Detection history table
* Weekly activity trends

---

# 💼 Project Impact & Key Achievements

### SmartRoadAI – Edge AI Road Monitoring Platform

* Developed an edge AI pothole detection system using OpenCV, TensorFlow Lite, and Google AI Edge LiteRT.
* Built a Flask-based analytics dashboard for monitoring detections and confidence metrics.
* Designed a Raspberry Pi-compatible deployment architecture for edge inference.
* Implemented an event logging pipeline with historical analytics and activity tracking.
* Deployed a cloud-hosted monitoring dashboard using Render.
* Utilized GitHub for version control and deployment workflows.

---

# 🔮 Future Improvements

* SQLite/PostgreSQL integration
* GPS-based pothole localization
* Interactive map visualization
* Severity classification
* Mobile application support
* Cloud synchronization
* Smart city infrastructure integration

---

# Author

Uday Soni
