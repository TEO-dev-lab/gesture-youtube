# gesture_detector.py
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from config import SWIPE_THRESHOLD

class GestureDetector:
    def __init__(self):
        self.threshold = SWIPE_THRESHOLD
        self.prev_x = None
        self.swipe_cooldown = 0
        
        # Download the model automatically
        self.model_path = "hand_landmarker.task"
        self._download_model()
        
        # Initialize HandLandmarker
        base_options = python.BaseOptions(model_asset_path=self.model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1,
            min_hand_detection_confidence=0.7,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        
        # Colors for drawing
        self.colors = {
            'green': (0, 255, 0),
            'red': (0, 0, 255),
            'blue': (255, 0, 0),
            'yellow': (0, 255, 255)
        }
        
    def _download_model(self):
        """Downloads the hand_landmarker.task model if it doesn't exist"""
        import urllib.request
        import os
        
        if not os.path.exists(self.model_path):
            print("Downloading hand_landmarker.task model...")
            url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
            urllib.request.urlretrieve(url, self.model_path)
            print("Model loaded!")
    
    def _draw_landmarks(self, frame, hand_landmarks):
        """Draws the hand landmarks on the frame using OpenCV"""
        h, w, _ = frame.shape
        
        # List of connections between hand landmarks
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),  # Thumb
            (0, 5), (5, 6), (6, 7), (7, 8),  # Index finger
            (0, 9), (9, 10), (10, 11), (11, 12),  # Middle
            (0, 13), (13, 14), (14, 15), (15, 16),  # Ring
            (0, 17), (17, 18), (18, 19), (19, 20),  # Pinky
            (5, 9), (9, 13), (13, 17)  # Connections between fingers
        ]
        
        # Draw connections
        for idx1, idx2 in connections:
            if idx1 < len(hand_landmarks) and idx2 < len(hand_landmarks):
                x1 = int(hand_landmarks[idx1].x * w)
                y1 = int(hand_landmarks[idx1].y * h)
                x2 = int(hand_landmarks[idx2].x * w)
                y2 = int(hand_landmarks[idx2].y * h)
                cv2.line(frame, (x1, y1), (x2, y2), self.colors['green'], 2)
        
        # Draw points
        for idx, landmark in enumerate(hand_landmarks):
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            # Different colors for different parts of the hand
            if idx == 0:  # Wrist
                cv2.circle(frame, (x, y), 8, self.colors['yellow'], -1)
            elif idx % 4 == 0:  # Fingertips (4, 8, 12, 16, 20)
                cv2.circle(frame, (x, y), 5, self.colors['red'], -1)
            else:
                cv2.circle(frame, (x, y), 3, self.colors['blue'], -1)
    
    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        
        result = self.detector.detect(mp_image)
        gesture = None
        
        if self.swipe_cooldown > 0:
            self.swipe_cooldown -= 1
        
        if result.hand_landmarks:
            for idx, hand_landmarks in enumerate(result.hand_landmarks):
                # Draw landmarks
                self._draw_landmarks(frame, hand_landmarks)
                
                # Check the right hand
                if result.handedness and idx < len(result.handedness):
                    handedness = result.handedness[idx][0].category_name
                    if handedness != "Right":
                        cv2.putText(frame, "LEFT HAND - Use RIGHT!", (50, 80), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        self.prev_x = None
                        return frame, None
                    else:
                        cv2.putText(frame, "RIGHT HAND ✓", (50, 80), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Wrist coordinates (point 0)
                h, w, _ = frame.shape
                wrist = hand_landmarks[0]
                curr_x = int(wrist.x * w)
                curr_y = int(wrist.y * h)
                
                # Point at the wrist (already drawn in _draw_landmarks)
                cv2.putText(frame, "WRIST", (curr_x - 30, curr_y - 25), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                
                # Swipe detection
                if self.prev_x is not None and self.swipe_cooldown == 0:
                    delta_x = curr_x - self.prev_x
                    
                    if delta_x < -self.threshold:
                        gesture = "next"
                        self.swipe_cooldown = 10
                        cv2.putText(frame, "Swipe Left → NEXT", (50, 50), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                    elif delta_x > self.threshold:
                        gesture = "prev"
                        self.swipe_cooldown = 10
                        cv2.putText(frame, "Swipe Right → PREV", (50, 50), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                    
                    # Direction arrow
                    if abs(delta_x) > 15:
                        cv2.arrowedLine(frame, 
                                       (curr_x - delta_x//2, curr_y - 30), 
                                       (curr_x - delta_x, curr_y - 30), 
                                       (255, 255, 0), 2, tipLength=0.3)
                
                self.prev_x = curr_x
        else:
            self.prev_x = None
            cv2.putText(frame, "Show your right hand", (50, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Bottom information on the screen
        cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame, gesture