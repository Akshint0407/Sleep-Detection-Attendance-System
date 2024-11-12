import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import Label
import cv2
from PIL import Image, ImageTk
import threading
from sleep_detection import detect_sleep
from camera_input import get_camera_input
from video_image_input import load_video, load_image

# Main application class for sleep detection
class SleepDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sleep Detection")  # Set window title
        self.root.geometry("600x400")  # Set window size

        # Title label for the application
        title_label = tk.Label(root, text="Sleep Detection", font=("Arial", 24, "bold"), pady=20)
        title_label.pack()

        # Buttons for selecting real-time detection, video, and image input
        real_time_btn = tk.Button(root, text="Detect Sleep Real Time", command=self.detect_real_time, width=25, height=2)
        real_time_btn.pack(pady=10)

        video_btn = tk.Button(root, text="Detect from Saved Video", command=self.load_video_file, width=25, height=2)
        video_btn.pack(pady=10)

        image_btn = tk.Button(root, text="Detect from Saved Image", command=self.load_image_file, width=25, height=2)
        image_btn.pack(pady=10)

        # Image panel to show thumbnail of video/image
        self.image_panel = tk.Label(root)
        self.image_panel.pack(pady=20)

    def detect_real_time(self):
        # Initiates real-time sleep detection
        self.show_loading_dialog("Analyzing real-time sleep detection...")
        threading.Thread(target=self._analyze_real_time).start()

    def _analyze_real_time(self):
        # Processes frames from the camera to detect sleep
        try:
            frames = get_camera_input(50)  # Capture 50 frames
            is_sleep, status = detect_sleep(frames)
            self.show_result_dialog(is_sleep, status)
        except Exception as e:
            self.show_error_dialog(str(e))

    def load_video_file(self):
        # Open file dialog to select a video file
        file_path = filedialog.askopenfilename(title="Select a video file", filetypes=[("Video files", "*.mp4 *.avi")])
        if file_path:
            self.show_loading_dialog("Analyzing video...")
            threading.Thread(target=self._analyze_video, args=(file_path,)).start()

    def _analyze_video(self, video_path):
        # Analyzes the selected video file for sleep detection
        try:
            result = load_video(video_path)
            self.display_thumbnail(video_path, result)
            self.show_result_dialog(result[0], result[1])
        except Exception as e:
            self.show_error_dialog(str(e))

    def load_image_file(self):
        # Open file dialog to select an image file
        file_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.jpg *.png")])
        if file_path:
            self.show_loading_dialog("Analyzing image...")
            threading.Thread(target=self._analyze_image, args=(file_path,)).start()

    def _analyze_image(self, image_path):
        # Analyzes the selected image for sleep detection
        try:
            result = load_image(image_path)
            self.display_thumbnail(image_path, result)
            self.show_result_dialog(result[0], result[1])
        except Exception as e:
            self.show_error_dialog(str(e))

    def show_loading_dialog(self, message):
        # Shows a dialog while processing is ongoing
        self.loading_dialog = tk.Toplevel(self.root)
        self.loading_dialog.title("Processing")
        tk.Label(self.loading_dialog, text=message).pack(pady=20)
        self.loading_dialog.geometry("300x100")
        self.loading_dialog.transient(self.root)
        self.loading_dialog.grab_set()

    def show_result_dialog(self, is_sleep, status):
        # Displays the result of the sleep detection
        if self.loading_dialog:
            self.loading_dialog.destroy()  # Close the loading dialog

        # Determine the message based on detection results
        if status == 0:
            message = "No human present."
        elif is_sleep:
            message = "Person was sleeping."
        else:
            message = "Person is awake."

        messagebox.showinfo("Result", message)

    def show_error_dialog(self, error_message):
        # Shows an error message if an exception occurs
        if self.loading_dialog:
            self.loading_dialog.destroy()  # Close the loading dialog
        messagebox.showerror("Error", error_message)

    def display_thumbnail(self, file_path, result):
        """Display the image or video thumbnail with the result caption."""
        # Load and display the thumbnail
        image = cv2.imread(file_path)
        if image is not None:
            image = cv2.resize(image, (200, 150))  # Resize for thumbnail display
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert color format
            image = ImageTk.PhotoImage(Image.fromarray(image))  # Convert to Tkinter format
            self.image_panel.config(image=image)
            self.image_panel.image = image  # Keep a reference

            # Set caption based on the result
            caption = "No Human" if result[1] == 0 else ("Sleeping" if result[0] else "Awake")

            # Update or create caption label
            if hasattr(self, 'caption_label'):
                self.caption_label.config(text=caption)
            else:
                self.caption_label = Label(self.root, text=caption, font=("Arial", 14))
                self.caption_label.pack(pady=10)


# Entry point for running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SleepDetectionApp(root)
    root.mainloop()
