Markdown

# 🚗 Real-Time Pothole Detector (Raspberry Pi & Picamera2)

A lightweight computer vision system designed to detect road potholes in real-time. This project uses a custom-trained, INT8-quantized YOLO model running via Google's `ai-edge-litert`. 



It is specifically built for modern Raspberry Pi OS environments (Bullseye, Bookworm, or Debian Trixie) and natively utilizes the `Picamera2` library for high-performance hardware camera access.

## ✨ Key Features
* **Google AI Edge LiteRT:** Utilizes the newest runtime for fast, optimized inference on ARM architectures.
* **Native Picamera2 Support:** Directly hooks into the Pi's `libcamera` system for low-latency video capture without the need for legacy camera workarounds.
* **Event Logging:** Records the exact timestamp and confidence score of detected potholes to a `pothole_events.csv` file. Includes a cooldown timer to prevent spamming the log.
* **Video Fallback:** Can process pre-recorded `.mp4` video files if a live camera is not available.

## 📁 Project Structure
* `main.py`: The main Python script to run the detector.
* `best-int8.tflite`: The INT8 quantized neural network model.
* `pothole_events.csv`: The auto-generated log file of detected potholes.
* `requirements.txt`: List of pip-installable dependencies.

## ⚙️ Installation & Setup

### The `Picamera2` Rule
`Picamera2` is deeply integrated into the Raspberry Pi OS and interacts directly with the hardware's `libcamera` stack. Because of this, **you cannot install it via pip**. If you try to run `pip install picamera2`, your project will break. 

Instead, we must create a virtual environment that is allowed to "borrow" the pre-installed `Picamera2` library directly from the Raspberry Pi's core system.

### 1. Clone the Repository
Open your Raspberry Pi terminal and run:
```bash
git clone [https://github.com/yourusername/pothole-detector.git](https://github.com/yourusername/pothole-detector.git)
cd pothole-detector
2. Create the Virtual Environment (Crucial Step)
You must include the --system-site-packages flag. This is the magic command that grants your isolated environment access to the system's Picamera2 files.

Bash

python3 -m venv venv --system-site-packages
3. Activate the Environment
Bash

source venv/bin/activate
(You should see (venv) appear at the beginning of your terminal prompt).

4. Install Requirements
With the environment active, install the standard Python packages:

Bash

pip install -r requirements.txt
(Note: Your requirements.txt should only contain opencv-python, numpy, and ai-edge-litert).

🚀 Usage
Make sure your virtual environment is active, then run the main script:

Bash

python main.py
Operation Modes
The terminal will prompt you to choose an input method:

Live Camera: Initializes the Pi Camera Module via Picamera2 (RGB888 format, 640x480 resolution).

Video File: Prompts you to enter the path to a video file (e.g., test_vid2.mp4).

Output
Display: Shows the live feed with red bounding boxes drawn around detected potholes, along with confidence scores and an FPS meter.

CSV Logging: Generates pothole_events.csv in the root folder.

Example CSV Output:

Code snippet

Timestamp,Confidence
2026-02-18 14:30:05,0.85
2026-02-18 14:30:15,0.72
🛠️ Troubleshooting Picamera2
If main.py crashes on startup when selecting Live Camera mode:

Check the Ribbon Cable: Ensure the camera cable is seated correctly in the Pi's CSI port with the silver contacts facing the HDMI ports.

Test the Camera Natively: Run libcamera-hello in your terminal. If this fails, your OS does not recognize the camera hardware, and you may need to check your /boot/firmware/config.txt file or update your system (sudo apt update && sudo apt upgrade).

Verify Environment: Ensure you remembered to use the --system-site-packages flag in Step 2.
