import cv2
import time
import os
from datetime import datetime

import config
from modules.camera import get_cap
from modules.motion_detector import MotionDetector
from modules.face_detector import FaceDetector
from modules.notify import send_async


def main():
    print(f"--- Security System Online [HEADLESS MODE] ---")


    while True:
        # 1. Camera Connection (RTSP/HTTP via IP Webcam)
        cap = get_cap(config.VIDEO_SOURCE)
        if cap is None:
            print("[!] CRITICAL: Camera not found. Retrying in 5s...")
            time.sleep(5)
            continue

        print("[+] Stream connected. Ready for action.")

        motion = MotionDetector()
        face = FaceDetector()

        recording = False
        video_out = None
        video_path = ""
        last_photo = 0
        last_motion = 0
        motion_start_time = 0

        try:
            while True:
                # --- BUFFER CLEANUP ---
                # Grab 10 frames to clear the queue and get real-time footage
                for _ in range(10):
                    cap.grab()
                ret, frame = cap.retrieve()

                if not ret:
                    print("[Warning] Stream disconnected. Reconnecting...")
                    break

                # Frame pre-processing
                frame = cv2.resize(frame, (640, 480))
                gray = cv2.GaussianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (21, 21), 0)

                # Motion Detection
                is_moving, _ = motion.has_motion(gray, config.SENSITIVITY, config.MIN_AREA, config.BG_UPDATE_ALPHA)

                now = time.time()
                if is_moving:
                    if last_motion == 0:
                        motion_start_time = now
                    last_motion = now

                    # --- SMART ALERT LOGIC ---
                    if (now - last_photo) > config.COOLDOWN:
                        # CAPTURE DELAY: Wait 2.0s after motion starts to catch the intruder's face
                        CAPTURE_DELAY = 2.0

                        if (now - motion_start_time) > CAPTURE_DELAY:
                            # Run face detection only for the snapshot
                            frame, face_found = face.draw_faces(frame, gray)

                            # 1. Instant Text Alert
                            alert_msg = f"⚠️ SECURITY ALERT: Movement detected at {datetime.now().strftime('%H:%M:%S')}!"
                            send_async(config.MESSAGE_URL, {"chat_id": config.CHAT_ID, "text": alert_msg}, {})

                            # 2. Delayed Photo Proof
                            _, buf = cv2.imencode(".jpg", frame)
                            send_async(config.PHOTO_URL, {"chat_id": config.CHAT_ID},
                                       {"photo": ("evidence.jpg", buf.tobytes())})

                            print(f"[Alert] Notification sent (Delay: {CAPTURE_DELAY}s). Face: {face_found}")
                            last_photo = now
                else:
                    motion_start_time = 0

                # --- VIDEO RECORDING LOGIC ---
                if is_moving or (recording and (now - last_motion < config.POST_MOTION_TIME)):
                    if not recording:
                        timestamp = datetime.now().strftime('%H%M%S')
                        filename = f"event_{timestamp}.avi"
                        video_path = os.path.join(config.CAPTURES_DIR, filename)

                        fourcc = cv2.VideoWriter_fourcc(*'XVID')
                        video_out = cv2.VideoWriter(video_path, fourcc, 15.0, (640, 480))
                        recording = True
                        print(f"[Video] Recording started: {filename}")

                    video_out.write(frame)
                else:
                    if recording:
                        # Close and send video
                        video_out.release()
                        recording = False
                        time.sleep(0.5)

                        print(f"[Video] Exporting capture to Telegram...")
                        try:
                            with open(video_path, "rb") as f:
                                video_bytes = f.read()

                            send_async(config.VIDEO_URL,
                                       {"chat_id": config.CHAT_ID},
                                       {"video": ("capture.avi", video_bytes)},
                                       video_path)
                        except Exception as e:
                            print(f"[Error] Failed to upload video: {e}")

                # Maintain low CPU usage
                time.sleep(0.01)

        except Exception as e:
            print(f"[Runtime Error] {e}")
            time.sleep(2)
        finally:
            cap.release()
            if video_out:
                video_out.release()


if __name__ == "__main__":
    main()