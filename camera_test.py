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

# def capture_image(camera, path):
#     camera.capture_file(path)
#     print(f"Captured image: {path}")

# async def time_lapse(TotalFrames, Interval, NAME):
#     # start camera & set camera state as false when time lapse is running
#     file_utils.write_boolean_to_file(APP_STATIC + '/CameraState.txt', False)
    
#     camera = Picamera2()
#     camera.configure(camera.create_still_configuration())
#     camera.start()
#     print("camera started")

#     try:
#         for i in range(TotalFrames):
#             # get the time to create the name of the file
#             timestr = time.strftime("%H%M%S", time.localtime())
#             imageName = timestr + NAME
#             print(imageName)
#             path = os.path.join(APP_STATIC, imageName)
#             update_log(imageName)

#             capture_image(camera, path)  # Now awaiting the async function
#             await asyncio.sleep(Interval)  # Wait for the interval second between captures
#     finally:
#         camera.stop()
        
#     # finish running time lapse camera state is true
#     return file_utils.write_boolean_to_file(APP_STATIC + '/CameraState.txt', True)

# async def run(TotalFrames, Interval, NAME):
#     await asyncio.gather(
#         asyncio.create_task(time_lapse(TotalFrames, Interval, NAME)),
#         # asyncio.create_task(upload_to_azure())
#     )
#     return

def capture_image(camera, path):
    """Capture an image and save it to the specified path."""
    camera.capture_file(path)
    print(f"Captured image: {path}")

async def time_lapse(TotalFrames, Interval, NAME):
    """Run a time-lapse sequence capturing images at specified intervals."""
    # Start camera & set camera state as false when time lapse is running
    file_utils.write_boolean_to_file(os.path.join(APP_STATIC, 'CameraState.txt'), False)
    
    camera = Picamera2()
    camera.configure(camera.create_still_configuration())
    print("Camera started")

    try:
        for i in range(TotalFrames):
            camera.start()
            # Get the current time to create the name of the file
            timestr = time.strftime("%H%M%S", time.localtime())
            imageName = f"{timestr}_{NAME}.jpg"  # Ensure a .jpg extension
            print(imageName)
            path = os.path.join(APP_STATIC, imageName)
            update_log(imageName) 

            # Capture the image in a separate thread
            capture_image(camera, path)
            camera.close()
            await asyncio.sleep(Interval)  # Wait for the specified interval between captures
    finally:
        camera.close()
        camera.stop()
        
    # Finish running time lapse, camera state is true    file_utils.write_boolean_to_file(os.path.join(APP_STATIC, 'CameraState.txt'), True)

async def run(TotalFrames, Interval, NAME):
    """Run the time-lapse and any other tasks concurrently."""
    await asyncio.gather(
        asyncio.create_task(time_lapse(TotalFrames, Interval, NAME)),
        # asyncio.create_task(upload_to_azure())  # Uncomment if you have this function
    )
