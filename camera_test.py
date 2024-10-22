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

async def capture_image(camera, imageName):
    camera.capture(imageName)
    print(f"Captured image: {imageName}")

async def time_lapse(TotalFrames, Interval, NAME):
    # start camera & set camera state as false when time lapse is running
    file_utils.write_boolean_to_file(APP_STATIC + '/CameraState.txt', False)
    
    camera = Picamera2()
    camera.configure(camera.create_still_configuration())
    camera.start()
    print("camera started")

    try:
        for i in range(TotalFrames):
            # image_name = f"image_{i}.jpg"
            print(i)
            # get the time to create the name of the file
            timestr = time.strftime("%H%M%S", time.localtime())
            imageName = timestr + NAME
            path = os.path.join(APP_STATIC, imageName)
            update_log(imageName)

            capture_image(camera, imageName)  # Now awaiting the async function
            await asyncio.sleep(Interval)  # Wait for 1 second between captures
    finally:
        camera.stop()
        
    # finish running time lapse camera state is true
    return file_utils.write_boolean_to_file(APP_STATIC + '/CameraState.txt', True)

async def run(TotalFrames, Interval, NAME):
    await asyncio.gather(
        asyncio.create_task(time_lapse(TotalFrames, Interval, NAME)),
        # asyncio.create_task(upload_to_azure())
    )
    return
