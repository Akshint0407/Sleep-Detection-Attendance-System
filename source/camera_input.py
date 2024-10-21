import cv2
import numpy as np


def get_camera_input(num_frames=300): # will return the number of frames you want usually a video has 30 fps
    """
    Capture video from the camera and return a list of processed frames.
    
    :param num_frames: Number of frames to capture
    :return: List of processed frames (grayscale)
    """
    cap = cv2.VideoCapture(0)  # Use 0 for default camera
    
    frames = []
    
    while len(frames) < num_frames:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture video.")
            break
    
        
        frames.append(frame)
        cv2.imshow("Camera Feed", frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            print("Exiting camera feed...")
            break
        
    cap.release()
    cv2.destroyAllWindows()  # Close all OpenCV windows
    return np.array(frames) 
