import cv2
import numpy as np
import time
import os
import datetime
import sys

# --------------------------------------------------
# Python 3.13 imp fix
# --------------------------------------------------
try:
    import imp
except ImportError:
    import types
    dummy_imp = types.ModuleType("imp")
    dummy_imp.reload = lambda x: x
    dummy_imp.find_module = lambda x: None
    sys.modules["imp"] = dummy_imp

# --------------------------------------------------
# Google Edge LiteRT
# --------------------------------------------------
from ai_edge_litert.interpreter import Interpreter
print("Using Google AI Edge LiteRT")

# --------------------------------------------------
# Picamera2
# --------------------------------------------------
from picamera2 import Picamera2

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
MODEL_PATH = "best-int8.tflite"
LOG_FILE = "pothole_events.csv"

THRESHOLD = 0.40
INPUT_SIZE = 320
COOLDOWN_SECONDS = 3.0

CAM_WIDTH = 640
CAM_HEIGHT = 480

# --------------------------------------------------
# INPUT SELECTION
# --------------------------------------------------
print("\n1. Live Camera")
print("2. Video File")
choice = input("Enter 1 or 2: ").strip()

video_mode = False

if choice == "2":
    video_path = input("Enter video filename: ").strip()
    if not os.path.exists(video_path):
        print("File not found.")
        sys.exit()
    cap = cv2.VideoCapture(video_path)
    video_mode = True
else:
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(
        main={"size": (CAM_WIDTH, CAM_HEIGHT), "format": "RGB888"}
    )
    picam2.configure(config)
    picam2.start()
    time.sleep(1)

# --------------------------------------------------
# LOAD MODEL (4 threads)
# --------------------------------------------------
interpreter = Interpreter(model_path=MODEL_PATH, num_threads=4)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

input_scale, input_zero = input_details[0]['quantization']
input_dtype = input_details[0]['dtype']

# --------------------------------------------------
# LOG FILE
# --------------------------------------------------
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("Timestamp,Confidence\n")

# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------
last_log_time = 0
prev_frame_time = 0

print("\nSystem Running\n")

while True:

    if video_mode:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    else:
        frame_rgb = picam2.capture_array()
        frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

    h_img, w_img = frame.shape[:2]

    # -------------------------
    # PREPROCESS
    # -------------------------
    img = cv2.resize(frame_rgb, (INPUT_SIZE, INPUT_SIZE))

    if input_scale > 0:
        input_data = ((img / 255.0) / input_scale + input_zero).astype(input_dtype)
    else:
        input_data = img.astype(np.float32) / 255.0

    input_data = np.expand_dims(input_data, axis=0)

    # -------------------------
    # INFERENCE
    # -------------------------
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])[0]

    # Dequantize
    out_scale, out_zero = output_details[0]['quantization']
    if out_scale > 0:
        output = (output.astype(np.float32) - out_zero) * out_scale

    pothole_detected = False
    max_conf = 0

    for det in output:
        conf = det[4]
        if len(det) > 5:
            conf *= det[5]

        if conf > THRESHOLD:
            pothole_detected = True
            max_conf = max(max_conf, conf)

            x, y, w, h = det[0:4]

            x_min = int((x - w/2) * w_img)
            y_min = int((y - h/2) * h_img)
            x_max = int((x + w/2) * w_img)
            y_max = int((y + h/2) * h_img)

            cv2.rectangle(frame, (x_min, y_min),
                          (x_max, y_max),
                          (0, 0, 255), 2)

    # -------------------------
    # LOGGING
    # -------------------------
    current_time = time.time()
    if pothole_detected and (current_time - last_log_time) > COOLDOWN_SECONDS:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp},{max_conf:.2f}\n")
        last_log_time = current_time

    # -------------------------
    # FPS
    # -------------------------
    new_frame_time = time.time()
    fps = 1 / (new_frame_time - prev_frame_time) if prev_frame_time else 0
    prev_frame_time = new_frame_time

    cv2.putText(frame, f"FPS: {int(fps)}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (255,255,0), 2)

    cv2.imshow("Pothole Detector - Picamera2", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

if video_mode:
    cap.release()

cv2.destroyAllWindows()
