import cv2
import time

def get_cap(source):
    """Initializes the video source and clears initial buffer."""
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        return None
    # Flush RTSP buffer
    for _ in range(5):
        cap.read()
    return cap