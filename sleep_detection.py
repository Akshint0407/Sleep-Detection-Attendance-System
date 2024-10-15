import cv2
import dlib
import numpy as np

# Constants for EAR calculation
EYE_AR_THRESH = 0.25  # Threshold for sleep detection
EYE_AR_CONSEC_FRAMES = 25  # Number of consecutive frames to confirm sleep

# Load Dlib's face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor_path = 'shape_predictor_68_face_landmarks.dat'  # model used
predictor = dlib.shape_predictor(predictor_path)

def calculate_eye_aspect_ratio(eye):
    """Calculate the Eye Aspect Ratio (EAR) for a given eye."""
    # Convert dlib points to numpy arrays
    eye_points = np.array([[p.x, p.y] for p in eye])

    # Calculate the distances between the eye landmarks
    A = np.linalg.norm(eye_points[1] - eye_points[5])  # Vertical distance
    B = np.linalg.norm(eye_points[2] - eye_points[4])  # Vertical distance
    C = np.linalg.norm(eye_points[0] - eye_points[3])  # Horizontal distance

    # Eye Aspect Ratio (EAR)
    ear = (A + B) / (2.0 * C)
    return ear

def preprocess_frame(frame):
    """Enhance the frame for better detection."""
    # Convert to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply histogram equalization
    equalized_frame = cv2.equalizeHist(gray_frame)

    # Convert back to BGR for further processing if needed
    return cv2.cvtColor(equalized_frame, cv2.COLOR_GRAY2BGR)

def detect_sleep(frames):
    """Detect sleep from the given frames and check for human presence."""
    sleep_counter = 0
    is_sleeping = False
    not_human_present = 0  # Count of frames with no human detected
    total_frames = len(frames)

    for i, frame in enumerate(frames):
        if frame is None or frame.size == 0:
            print("Received an empty frame.")
            continue  # Skip this frame

        # Preprocess the frame
        processed_frame = preprocess_frame(frame)

        # Check if a human is present
        faces = detector(processed_frame)
        if len(faces) == 0:
            print(f"No faces detected in frame {i}.")
            not_human_present += 1
            continue  # Continue to the next frame

        # Reset not human present counter if a face is detected
        not_human_present = 0

        for face in faces:
            # Get the landmarks for the detected face
            shape = predictor(processed_frame, face)
            landmarks = shape.parts()  # Assuming you're using dlib's face landmark prediction
            
            # Extract the left and right eye coordinates
            left_eye = np.array([landmarks[i] for i in range(36, 42)])  # Left eye landmarks
            right_eye = np.array([landmarks[i] for i in range(42, 48)])  # Right eye landmarks
            
            # Calculate EAR for both eyes
            ear_left = calculate_eye_aspect_ratio(left_eye)
            ear_right = calculate_eye_aspect_ratio(right_eye)
            ear = (ear_left + ear_right) / 2.0

            # Check if the user is sleeping
            if ear < EYE_AR_THRESH:
                sleep_counter += 1
                print(f"Frame {i}: Sleeping detected, EAR = {ear:.2f}.")
                if sleep_counter >= EYE_AR_CONSEC_FRAMES:
                    is_sleeping = True
                    break  # Exit if the person is detected sleeping
            else:
                print(f"Frame {i}: Not sleeping detected, EAR = {ear:.2f}.")
                sleep_counter = 0  # Reset counter if eyes are open

        if is_sleeping:
            break  # Exit the outer loop if sleeping is detected

    # Check if there were any frames with human presence
    if not_human_present >= total_frames // 2:
        print('No human present.')
        return (True, 0)  # 0 for no person present

    # Return status based on the detection results
    if is_sleeping:
        return (True, 1)  # 1 for person was present but sleeping
    return (False, 0)  # 0 for person present but not sleeping
