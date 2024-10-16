import picamera2
import asyncio
import RPi.GPIO as GPIO
import os
import time
from flask import Flask, render_template, Response, request, send_file, jsonify

# import custom library
import utils
# import azure_utils
import hw_utils

# set file directory
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

# init hardware setup
# hw_utils.light_init()
hw_utils.soil_sensor_init()

# create SoilState file if not exist 
if not os.path.exists(APP_STATIC + '/SoilState.txt'):
    sensorlog_f = open(APP+STATIC +'/SoilState.txt', 'a')
    sensorlog_f.write('filename, temperature (C), moisture' + "\n")
    sensorlog_f.close()
    print('SoilState.txt created')
else:
    print('SoilState.txt exist')

# create and clear Camera State text file 
camera_f = open(APP_STATIC + '/CameraState.txt', 'w')
camera_f.close()

def update_log(filename: str):
    log_f = open(APP_STATIC + '/log.txt', 'a')
    log_f.write(filename + "\n")
    log_f.close()
    return

# write on the soil log file
def soil_condition_log(filename: str):
    moisture = hw_utils.soilsensor.moisture_read()
    temp = hw_utils.soilsensor.get_temp()
    
    sensorlog_f = open(APP_STATIC + '/SoilState.txt', 'a')
    sensorlog_f.write(str(filename) + ", " + str(temp) + ", " + str(moisture) + "\n")
    sensorlog_f.close()
    return

# time lapse function
async def time_lapse(HolocamObj, TotalFrames, Interval, NAME):
    # start camera & set camera state as false when time lapse is running
    utils.write_boolean_to_file(APP_STATIC + '/CameraState.txt', False)
    
    for i in range(TotalFrames):
        # get the time to create the name of the file
        timestr = time.strftime("%H%M%S", time.localtime())
        imageName = timestr + NAME
        path = os.path.join(APP_STATIC, imageName)
        
        # capture image 
        HolocamObj.capture(path)
        
        # log soil sensor data on SoilState.txt
        # and image name for uploading
        soil_condition_log(imageName)
        update_log(imageName)
        
        await asyncio.sleep(Interval)
        
    # close camera after time lapse to avoid out of resources error
    #hw_utils.camera_close()
    HolocamObj.camera.close()
    
    # finish running time lapse camera state is true
    return utils.write_boolean_to_file(APP_STATIC + '/CameraState.txt', True)

# async def upload_to_azure():
#     # if the log is empty && camera state is true (done with Timelapse) then exit
#     while True:
#         logSize = os.stat(APP_STATIC +'/log.txt').st_size
#         cameraState = utils.read_boolean_from_file(APP_STATIC + '/CameraState.txt')
#         if cameraState and logSize == 0:
#             print("Done Uploading")
#             break
#         # if log is empty and time-lapse is not done (wait 1 second)
#         elif not cameraState and logSize == 0:
#             print("Waiting for picture")
#             await asyncio.sleep(1)
#         # else upload file to azure
#         else:
#             try:
#                 log_f = open(APP_STATIC + '/log.txt', 'r+')               
#                 #await asyncio.sleep(1)
#                 ImageList = log_f.readlines()
#                 filename = ImageList[0].strip('\n')

#                 await azure_utils.upload_to_azure_blob(filename)
                
#                 log_f.seek(0)
#                 log_f.truncate()
#                 log_f.writelines(ImageList[1:])
#                 log_f.close()
#             except:
#                  print("Time-lapse still going, but empty file")
#     return 

async def run(HolocamObj, TotalFrames, Interval, NAME):
    await asyncio.gather(
        asyncio.create_task(time_lapse(HolocamObj, TotalFrames, Interval, NAME)),
        # asyncio.create_task(upload_to_azure())
    )
    return


# from hw_utils import Holocam
# holocam = Holocam()
# 
# s = time.perf_counter()
# asyncio.run(run(holocam, 3, 3, 'test.jpg'))
# elapsed = time.perf_counter() - s
# print(f"{__file__} executed in {elapsed:0.2f} seconds.")

