import cv2
import numpy as np
from sleep_detection import detect_sleep  # Assuming detect_sleep is defined in another file

def load_video(video_path):
    """Loads a video file, extracts frames, and performs sleep detection on them."""
    cap = cv2.VideoCapture(video_path)
    frames = []

    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # End of video
        frames.append(frame)

    cap.release()
    cv2.destroyAllWindows()

    # Pass the frames to the sleep detection function
    result = detect_sleep(frames)
    return result
    #print(f"Sleep detection result from video: {result}")


def load_image(image_path):
    """Loads an image file and performs sleep detection on it."""
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error loading image file: {image_path}")
        return

    # Convert image into a list of one frame for compatibility with detect_sleep
    frames = [image]

    # Pass the image to the sleep detection function
    result = detect_sleep(frames, mode="image")
    return result
    #print(f"Sleep detection result from image: {result}")


if __name__ == "__main__":
    # Example usage
    video_path =  'test_file.mp4' # Change this to the path of your video
    image_path = "test_file_image.jpg"  # Change this to the path of your image

    load_video(video_path)  # Analyze the video
    load_image(image_path)  # Analyze the image
