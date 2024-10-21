import sys
import os
from tkinter import Tk

# Add the source folder to the system path so Python can find it
sys.path.append(os.path.join(os.path.dirname(__file__), 'source'))

from gui import SleepDetectionApp  

def start_gui():
    """Function to start the sleep detection GUI."""
    root = Tk()  # Create the main window
    root.title("Sleep Detection Application")  # Set window title
    
    # Initialize and start the GUI app
    app = SleepDetectionApp(root)
    root.mainloop()  # Start the Tkinter main loop

if __name__ == "__main__":
    start_gui()  # Start the GUI when this script is run
