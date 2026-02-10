![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![License](https://img.shields.io/badge/license-MIT-important.svg)
![Status](https://img.shields.io/badge/status-battle--tested-red.svg)

```markdown
## ⚖️ Disclaimer
This project was developed for **personal security purposes** within a private living space. The author is not responsible for any misuse of this software. Always comply with local privacy laws regarding video surveillance in shared environments.
```

# 🚨 Camera Security System

A lightweight Python-based surveillance system using OpenCV and Telegram API for real-time intruder detection.

## 📖 The Backstory

> This project was born out of necessity. While staying in a **youth refugee camp** in Germany, I faced a wave of thefts that even the security post and administration couldn't stop. To protect my equipment in this challenging environment, I developed this script and camouflaged a smartphone as an IP camera.

The system proved its worth on **February 10, 2026**. While I was on a different floor, I received a real-time alert on my phone. The script captured clear evidence of an intruder inside my room, allowing me to confront the individual immediately. 

The captured evidence was later handed over to the police to identify a serial thief who had been targeting the camp residents.

## 🛠️ Key Features
* **Real-time Motion Detection:** Optimized frame-differencing algorithm.
* **Instant Telegram Alerts:** Sends photo/video evidence directly to your device.
* **Headless Operation:** Runs discretely in the background.
* **Evidence Logging:** All captures are saved with precise timestamps.

> **Note:** This system was intentionally designed to be **simple and lightweight**. It was built quickly as a "Minimum Viable Product" (MVP) to solve an urgent security crisis with whatever resources were available at the moment.

## 🚀 Future Improvements (To-Do)
While the current version is effective, there is room for further development:
* **Advanced Face Recognition:** Integrating DeepFace or face_recognition libraries to distinguish between friends and intruders.
* **Cloud Backup:** Automatic uploading of captures to Google Drive or AWS S3 in case the local hardware is stolen.
* **Web Dashboard:** A simple Flask/FastAPI interface to view the live stream and history of alerts.
* **Smarter Trigger Zones:** Ability to define specific areas in the frame to monitor (ignoring pets or moving curtains).

 ## 💻 Tech Stack

The system is built with a focus on stability and low resource consumption, allowing it to run on older hardware or background processes.

* **Language:** Python 3.12+
* **Computer Vision:** * `OpenCV` (cv2) — used for frame analysis, grayscale conversion, and Gaussian blur to reduce noise.
* **Networking & Bot API:** * `Requests` — handles synchronous HTTP requests to the Telegram Bot API.
* **Video Source:** * `IP Webcam` (Android) — provides a stable MJPEG stream via local network.
* **Environment & OS:** * Developed in `PyCharm` (Windows), designed to be OS-independent (Linux/macOS ready).
    * Uses `.env` and `config.py` for secure credential management.
### 🧠 System Logic Flow
1. **Connect:** Establish stream with `IP Webcam` via HTTP/RTSP.
2. **Pre-process:** Convert frames to grayscale and apply Gaussian Blur to filter out "noise" (shadows, dust).
3. **Compare:** The system maintains a "running average" of the background. Any significant change triggers a contour detection.
4. **Action:** If the change area > `MIN_AREA`, the system captures a frame and fires an API request to Telegram.

### 1. Prepare the Video Source
* Install the **IP Webcam** app on an Android device.
* Start the server in the app.
* Note the IP address provided (e.g., `http://192.168.1.15:8080/video`).

### 2. Telegram Bot Setup
* Message [@BotFather](https://t.me/botfather) on Telegram and create a new bot.
* Copy the `API TOKEN`.
* Get your `CHAT_ID` 

### 3. Project Architecture & Structure

The system is modularized to separate camera handling, motion detection, and notifications.

```text
CameraSecuritySystem/
├── modules/
│   ├── __init__.py
│   ├── camera.py          # Handles the MJPEG stream connection
│   ├── motion_detector.py # Logic for frame differencing & movement triggers
│   ├── face_detector.py   # (Optional) Face detection logic
│   └── notify.py          # Telegram Bot API integration
├── captures/              # Local storage for all detected events (photos/videos)
├── main.py                # Entry point: integrates all modules into a loop
├── config.py              # Local config (ignored by git for security)
└── .gitignore             # Tells git to ignore .venv, config.py, and captures/
```

### 4.⚙️ Configuration & Environment Variables

The system uses an `.env` file and `os.getenv` for security, preventing sensitive tokens from being leaked. Below is the breakdown of the core settings:

#### 1. Security & Telegram
* `TOKEN` / `CHAT_ID`: Credentials used to authenticate with the Telegram Bot API.
* `PHOTO_URL` / `VIDEO_URL`: Dedicated endpoints for sending instant visual evidence.

#### 2. Detection Logic (The "Brain")
* `MIN_AREA (5000)`: The minimum size of an object (in pixels) to trigger an alert. This prevents the system from reacting to small insects or light flickering.
* `SENSITIVITY (25)`: Threshold for pixel intensity change.
* `BG_UPDATE_ALPHA (0.05)`: How fast the system "learns" the background. A higher value helps the system ignore stationary changes (like a chair being moved).

#### 3. Capture Timing
* `COOLDOWN (30s)`: Prevents spamming your phone. After an alert, the system waits 30 seconds before sending another.
* `POST_MOTION_TIME (4s)`: The amount of video recorded *after* the last motion is detected to ensure the full event is captured.

#### 4. Automated File Management
The script includes an automated check for the storage directory:
```python
if not os.path.exists(CAPTURES_DIR):
    os.makedirs(CAPTURES_DIR)
```

### 🛡️ Security First: Using .env
To keep your credentials safe, this project uses `python-dotenv`. 

1. Create a `.env` file in the root directory.
2. Add your sensitive data:
   ```text
   TOKEN=your_bot_token
   CHAT_ID=your_id
   ```

   
   
### 4. Clone and Install
```bash
# Clone the repository
git clone [https://github.com/holydynamited/CameraSecuritySystem.git](https://github.com/holydynamited/CameraSecuritySystem.git)
cd CameraSecuritySystem
