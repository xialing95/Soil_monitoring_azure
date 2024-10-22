import time
import os
import time
import file_utils
import threading
import numpy as np

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality

# set file directory
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

# create and clear Camera State text file 
camera_config = open(APP_STATIC + '/CameraState.txt', 'w')
camera_config.close()

def update_log(filename: str):
    log_f = open(APP_STATIC + '/log.txt', 'a')
    log_f.write(filename + "\n")
    log_f.close()
    return

def preview():
    picam2 = Picamera2()
    picam2.start()

    metadata = picam2.capture_file("static/preview.jpg")
    print(metadata)

    picam2.close()

def capture_image(camera, path):
    """Capture an image and save it to the specified path."""
    camera.capture_file(path)
    print(f"Captured image: {path}")

# Function to capture images
def capture_timelapse(interval, duration, NAME):
    picam2 = Picamera2()
    picam2.start()  # Start the camera

    end_time = time.time() + duration
    while time.time() < end_time:
        # Get the current time to create the name of the file
        timestr = time.strftime("%m-%d-%H%M%S", time.localtime())
        imageName = f"{timestr}-{NAME}" 
        path = os.path.join(APP_STATIC, imageName)

        # Capture both DNG and JPG images
        request = picam2.capture_request()
        request.save("main", 'static/preview.jpg')
        print(f"file name: {imageName}")
                
        # Save raw image data
        raw_buffer = request.make_buffer("raw")
        raw_data = np.frombuffer(raw_buffer, dtype=np.uint16)
        np.save(path, raw_data)

        request.release()  # Release the request
        time.sleep(interval)  # Wait for the specified interval

    picam2.stop()  # Stop the camera

# Main function
def time_lapse(inputDuration, inputInterval, NAME):
    interval = inputInterval  # Interval in seconds between captures
    duration = inputDuration  # Total duration of the timelapse in seconds

    # Start the capture in a separate thread
    timelapse_thread = threading.Thread(target=capture_timelapse, args=(interval, duration, NAME))
    timelapse_thread.start()

    # Main program can continue doing other things here
    print("Timelapse is running in the background...")

    # Optionally, wait for the thread to finish
    timelapse_thread.join()
    print("Timelapse capture completed.")


