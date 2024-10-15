import time
from camera_input import get_camera_input
from sleep_detection import detect_sleep

def main():
    num_frames = 50  # Adjust based on your requirements
    print("Starting camera input. Press Ctrl + D to stop.")
    
    try:
        while True:
            # Capture frames
            frames = get_camera_input(num_frames)
            is_sleeping = detect_sleep(frames)

                
            if is_sleeping[0]:
                if is_sleeping[1] == 0:
                    print("No person detected")
                else:
                    print('person is sleeping')
            else:
                print("person is awake")
            

            time.sleep(1)

    except EOFError:
        print("\nStopping detection...")


if __name__ == "__main__":
    main()