# main.py
import cv2
from gesture_detector import GestureDetector
from key_simulator import KeySimulator
from config import CAMERA_ID, FRAME_WIDTH, FRAME_HEIGHT,DEMONSTRATE_CAMERA

def main():
    # Init
    cap = cv2.VideoCapture(CAMERA_ID)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    
    detector = GestureDetector()
    keys = KeySimulator()

    print("Launch YouTube Shorts with gestures")
    print("Use your RIGHT hand")
    print("Swipe left → next video")
    print("Swipe right → previous video")
    print("Press 'q' to exit")
    print("-" * 40)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to get camera")
            break
        
        # Mirror reflection (for natural control)
        frame = cv2.flip(frame, 1)
        
        # Gesture processing
        frame, gesture = detector.detect(frame)
        
        # Perform the action
        if gesture == "next":
            keys.next_video()
        elif gesture == "prev":
            keys.prev_video()
        #Show the window from the camera if specified in the config
        if DEMONSTRATE_CAMERA:
            cv2.imshow("Gesture YouTube Shorts", frame)
        
        #Exit by pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Program completed")

if __name__ == "__main__":
    main()