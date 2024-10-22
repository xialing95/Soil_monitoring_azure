import time
import subprocess
import asyncio
import os
import time
import file_utils

from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs.fileoutput import FileOutput

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

# async def time_lapse(TotalFrames, Interval, NAME):
#     """Run a time-lapse sequence capturing images at specified intervals."""
#     # Start camera & set camera state as false when time lapse is running
#     # file_utils.write_boolean_to_file(os.path.join(APP_STATIC, 'CameraState.txt'), False)
    
#     camera = Picamera2()
#     capture_config = camera.create_still_configuration(raw={}, display=None)
#     print("Camera started")
#     camera.start()

#     # Give time for Aec and Awb to settle, before disabling them
#     time.sleep(1)
#     camera.set_controls({"AeEnable": False, "AwbEnable": False, "FrameRate": 1.0})
#     # And wait for those settings to take effect
#     time.sleep(1)

#     try:
#         for i in range(TotalFrames):
#             # Get the current time to create the name of the file
#             timestr = time.strftime("%m-%d-%H%M%S", time.localtime())
#             imageName = f"{timestr}_{NAME}" 
#             path = os.path.join(APP_STATIC, imageName)
#             # update_log(imageName) 
#             print(f"image #{i}, file name: {imageName}")
        
#             try:
#                 r = camera.switch_mode_capture_request_and_stop(capture_config)
#                 r.save ("main", "newest.jpg")
#                 r.save_dng(f"{path}.dng")
#             except asyncio.TimeoutError:
#                 print("Camera capture request timed out")
#             except Exception as e:
#                 print (f"Error during capture: {e}")
#             await asyncio.sleep(Interval)  # Wait for the specified interval between captures
#     finally:
#         camera.stop()
#         print("Done TimeLapse")
        
#         # Finish running time lapse, camera state is true
#         # file_utils.write_boolean_to_file(os.path.join(APP_STATIC, 'CameraState.txt'), True)

# async def run(TotalFrames, Interval, NAME):
#     """Run the time-lapse and any other tasks concurrently."""
#     await asyncio.gather(
#         asyncio.create_task(time_lapse(TotalFrames, Interval, NAME)),
#         # asyncio.create_task(upload_to_azure())  # Uncomment if you have this function
#     )

# def time_lapse(TotalFrames, Interval, NAME):
#     camera = Picamera2()
#     capture_config = camera.create_still_configuration(raw={}, display=None)
#     print("Camera started")
#     camera.start()

#     # Give time for Aec and Awb to settle, before disabling them
#     time.sleep(1)
#     camera.set_controls({"AeEnable": False, "AwbEnable": False, "FrameRate": 1.0})
#     # And wait for those settings to take effect
#     time.sleep(1)

#     try:
#         for i in range(TotalFrames):
#             # Get the current time to create the name of the file
#             timestr = time.strftime("%m-%d-%H%M%S", time.localtime())
#             imageName = f"{timestr}_{NAME}" 
#             path = os.path.join(APP_STATIC, imageName)
#             # update_log(imageName) 
#             print(f"image #{i}, file name: {imageName}")
        
#             try:
#                 r = camera.switch_mode_capture_request_and_stop(capture_config)
#                 r.save ("main", "newest.jpg")
#                 r.save_dng("newest.dng")
#             except Exception as e:
#                 print (f"Error during capture: {e}")
#             time.sleep(5)  # Wait for the specified interval between captures
#     finally:
#         camera.stop()
#         print("Done TimeLapse")

import threading
import numpy as np

# Function to capture images
def capture_timelapse(interval, duration, NAME):
    picam2 = Picamera2()
    picam2.start()  # Start the camera

    end_time = time.time() + duration
    while time.time() < end_time:
        # Get the current time to create the name of the file
        timestr = time.strftime("%m-%d-%H%M%S", time.localtime())
        imageName = f"{timestr}_{NAME}" 
        path = os.path.join(APP_STATIC, imageName)
        # update_log(imageName) 

        # Capture both DNG and JPG images
        request = picam2.capture_request()
        request.save("main", 'newest.jpg')
        print(f"file name: {imageName}")
                
        # Save raw image data
        raw_buffer = request.make_buffer("raw")
        raw_data = np.frombuffer(raw_buffer, dtype=np.uint16)
        np.save(imageName, raw_data)

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


