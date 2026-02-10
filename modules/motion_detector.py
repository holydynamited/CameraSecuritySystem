import cv2


class MotionDetector:
    def __init__(self):
        self.avg_frame = None

    def has_motion(self, gray_frame, sensitivity, min_area, alpha):
        """Returns (bool: detected, processed_diff_frame)."""
        if self.avg_frame is None:
            self.avg_frame = gray_frame.copy().astype("float")
            return False, None

        cv2.accumulateWeighted(gray_frame, self.avg_frame, alpha)
        delta = cv2.absdiff(gray_frame, cv2.convertScaleAbs(self.avg_frame))

        _, thresh = cv2.threshold(delta, sensitivity, 255, cv2.THRESH_BINARY)
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            if cv2.contourArea(c) > min_area:
                return True, delta
        return False, delta