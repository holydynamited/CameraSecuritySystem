import cv2

class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    def draw_faces(self, frame, gray_frame):
        """Detects faces and draws rectangles. Returns frame."""
        faces = self.face_cascade.detectMultiScale(gray_frame, 1.1, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        return frame, len(faces) > 0