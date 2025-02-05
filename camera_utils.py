import time
import os
import time
import json
import file_utils
import threading
import numpy as np
import RPi.GPIO as GPIO

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality

# set file directory
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

# create and clear Camera State text file 
camera_config = open(APP_STATIC + '/CameraState.txt', 'w')
camera_config.close()

def laser_on(LASER_PIN = 4): #GPIO4, pin 7
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LASER_PIN, GPIO.OUT)
    GPIO.output(LASER_PIN, True)
    print("Laser ON")
    return

def laser_off(LASER_PIN = 4):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LASER_PIN, GPIO.OUT)
    GPIO.output(LASER_PIN, False)
    print("Laser OFF")
    return

def update_log(filename: str):
    log_f = open(APP_STATIC + '/log.txt', 'a')
    log_f.write(filename + "\n")
    log_f.close()
    return

def preview():
    laser_on()
    time.sleep(3)
    picam2 = Picamera2()

    # Load camera settings from JSON file
    with open('camera_config.json', 'r') as f:
        config = json.load(f)

    # Configure camera settings
    picam2.configure(picam2.create_preview_configuration())
    # Set camera resolution
    picam2.set_controls({"Resolution": tuple(config["resolution"])})
    # Set ISO
    picam2.set_controls({"ISO": config["iso"]})
    # Set shutter speed (in microseconds)
    picam2.set_controls({"ExposureTime": config["expSpd"]})
    # Set frame rate
    picam2.set_controls({"FrameRate": config["framerate"]})
    # Set AWB settings
    if config["awbMod"] == "off":
        picam2.set_controls({"AwbMode": "off", "AwbGain": config["awbGain"]})
    
    time.sleep(2)
    picam2.start()

    metadata = picam2.capture_file("static/preview.jpg")
    print(metadata)

    picam2.close()
    laser_off()

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
        #turn laser on
        laser_on()

        # Get the current time to create the name of the file
        timestr = time.strftime("%m-%d-%H%M%S", time.localtime())
        imageName = f"{timestr}-{NAME}" 
        path = os.path.join(APP_STATIC, imageName)

        # Capture both DNG and JPG images
        request = picam2.capture_request()
        request.save("main", 'static/preview.jpg')
        print(f"file name: {imageName}")
                
        # Save raw image data
        # raw_array = request.make_array("raw")
        # raw_data = np.save(path, raw_array)
        # np.save(path, raw_data)

        request.save_dng(path)

        request.release()  # Release the request
        time.sleep(interval)  # Wait for the specified interval

    picam2.stop()  # Stop the camera
    laser_off()

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


