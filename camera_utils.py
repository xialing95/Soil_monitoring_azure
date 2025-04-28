import time
import os
import time
import json
import file_utils
import threading
import numpy as np
import RPi.GPIO as GPIO

from picamera2 import Picamera2
from picamera2.controls import Controls

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
    
    try:
        with Picamera2() as picam2:  # Context manager ensures cleanup
            # Load camera settings first
            with open('CAMERASETTING.json', 'r') as f:
                config = json.load(f)

            # Configure camera
            resolution = tuple(config.get("resolution", [1920, 1080]))
            preview_config = picam2.create_preview_configuration(main={"size": resolution})
            picam2.configure(preview_config)
            picam2.start()

            # Set camera controls
            try: 
                ctrls = Controls(picam2)
                ctrls.AnalogueGain = config["awbGain"]
                ctrls.ExposureTime = config["expSpd"]
                ctrls.Brightness = config["iso"]
                picam2.set_controls(ctrls)
                print("Settings changed successfully")
            except (RuntimeError, KeyError) as e:
                print(f"Control error: {e} (using defaults?)")

            # Let settings take effect
            time.sleep(1)
            
            # Capture preview
            metadata = picam2.capture_file("static/preview.jpg")
            print(metadata)

    except Exception as e:
        print(f"Camera error: {e}")
    finally:
        laser_off()  # Ensure laser always turns off
    return

def capture_image(camera, path):
    """Capture an image and save it to the specified path."""
    camera.capture_file(path)
    print(f"Captured image: {path}")
    return

#Check disk space (if it is less than 2mb, it will not be able to save the image)
def check_disk_space(directory, required_space_mb=200):
    """Check if there is enough disk space in the specified directory."""
    statvfs = os.statvfs(directory)
    free_space_mb = (statvfs.f_bavail * statvfs.f_frsize) / (1024 * 1024)
    return free_space_mb >= required_space_mb

# Function to capture images
def capture_timelapse(interval, duration, NAME):
    from picamera2 import Picamera2

    with Picamera2() as picam2:
        picam2.start()
        frame_count = 0
        expected_frame_count = int(duration / interval)

        if not check_disk_space(APP_STATIC):
            print("Not enough disk space to save images. Minimal 200mb")
            return

        start_time = time.time()
        while (time.time() - start_time) < duration:
            laser_on()
            timestr = time.strftime("%m-%d-%H%M%S", time.localtime())
            imageName = f"{timestr}-{NAME}"
            path = os.path.join(APP_STATIC, imageName)

            request = picam2.capture_request()
            request.save("main", 'static/preview.jpg')
            print(f"file name: {imageName}")
            request.save_dng(path)
            frame_count += 1

            request.release()
            time.sleep(interval)

        if frame_count == expected_frame_count:
            print("Success! Captured the expected number of images.")
        else:
            print(f"Warning: Did not capture expected number of images.")

        laser_off()

# def capture_timelapse(interval, duration, NAME):
#     picam2 = Picamera2()
#     picam2.start()  # Start the camera
#     frame_count = 0
#     expected_frame_count = int(duration/interval)

#     if not check_disk_space(APP_STATIC):
#         print("Not enough disk space to save images. Minimal 200mb")
#         return

#     # second from epoch time + duration in seconds
#     start_time = time.time()
#     while (time.time()-start_time) < duration:
#         #turn laser on
#         laser_on()

#         # Get the current time to create the name of the file
#         timestr = time.strftime("%m-%d-%H%M%S", time.localtime())
#         imageName = f"{timestr}-{NAME}" 
#         path = os.path.join(APP_STATIC, imageName)

#         # Capture both DNG and JPG images
#         request = picam2.capture_request()
#         request.save("main", 'static/preview.jpg')
#         print(f"file name: {imageName}")
                
#         # Save raw image data
#         # raw_array = request.make_array("raw")
#         # raw_data = np.save(path, raw_array)
#         # np.save(path, raw_data)

#         request.save_dng(path)
#         frame_count += 1

#         request.release()  # Release the request
#         time.sleep(interval)  # Wait for the specified interval

#     if frame_count == expected_frame_count:
#         print ("Success! Captured the expected number of images.")
#     else: 
#         print(f"Warning: Did not capture expect number of images.")
    
#     picam2.stop()  # Stop the camera
#     del picam2
#     print ("Stop the picamera")
#     laser_off()
#     return 

# Time Lapse Main function
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
    return
