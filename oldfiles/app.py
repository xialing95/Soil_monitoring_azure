#!/usr/bin/env python
from picamera import PiCamera
from os import system
import os
from time import sleep
from importlib import import_module
import datetime
import subprocess
from flask import Flask, render_template, Response, request, send_file, jsonify
import utils

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
laser = 5
bottonSts = GPIO.LOW
GPIO.setup(laser, GPIO.OUT)


# # import camera driver. Otherwise use pi camera by default
# if os.environ.get('CAMERA'):
#     Camera = import_module('camera_' + os.environ['CAMERA']).Camera
# else:
#     from camera_pi import Camera

system('rm static/*.jpg') #delete all photos in the Pictures folder before timelapse start
filepath = ('/static/')


# log_f = open('static/log.txt', 'w')
# log_f.close()

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

@app.route('/')
def index():
    """Video streaming home page."""
    log_f = open(os.path.join(APP_STATIC, 'log.txt'), 'r')
    logs = log_f.readlines()[0]    
    image_path = str(filepath + logs)
    print(image_path)
    return render_template('index.html', filename = image_path)
    

# def gen(filepath):
#     """Video streaming generator function."""
#     while True:
#         #frame = camera.get_frame()
#         frame = get_file(filepath)
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
# 
# @app.route('/video_feed')
# def video_feed():
#     """Video streaming route. Put this in the src attribute of an img tag."""
#     return Response(gen(Camera()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')
# 
# @app.route('/image_feed')
# def image_feed():
#     log_f = open(os.path.join(APP_STATIC, 'log.txt'), 'r')
#     logs = log_f.readlines()[0]    
#     image_path = str(filepath + logs)
#     print(image_path)
#     return render_template('index.html', filename = image_path)
camera.close()
camera = PiCamera()
sleep(2)
camera.resolution = (1024, 768)

@app.route('/time_lapse', methods=['GET', 'POST'])
def time_lapse():

    dateraw= datetime.datetime.now()
    datetimeformat = dateraw.strftime("%m-%d_%H:%M")
    print("RPi started taking photos for your timelapse at: " + datetimeformat)
    
    #set this to the number of minutes you wish to run your timelapse camera
    tlminutes = float(request.form.get('duration'))
    #number of seconds delay between each photo taken
    secondsinterval = int(request.form.get('interval'))
    filename = request.form.get('filename')
    arguments = request.form.get('arguments')
    #number of photos to take
    numphotos = int((tlminutes*60)/secondsinterval) 
    print("number of photos to take = ", numphotos)
    
    
        
    print("Done taking photos.")
    camera.close()
    GPIO.cleanup()

    #return render_template('index.html', filename = imagepath)
    return Response(gen(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame') 

def gen():
    for i in range(6):
        imagefilename = str(i)+'test.jpg'
        imagepath = os.path.join(APP_STATIC, imagefilename)
        
        GPIO.output(laser, True)
        camera.capture('static/'+imagefilename.format(i))
        GPIO.output(laser, False)

        # utils.upload_to_azure_blob(imagefilename)
        
        # save the newest photo name to the log 
        log_f = open('static/log.txt', 'a')
        log_f.truncate(0)
        log_f.write(imagefilename)
        log_f.close()
        
        sleep(1)
        print("Done taking photos.")
        camera.close()
        GPIO.cleanup()
        yield (b'--frame\r\n' 
              b'Content-Type: image/jpeg\r\n\r\n' + open('pic.jpg', 'rb').read() + b'\r\n')      

#asyncio.run(take_image())
async def take_image():
    task = asyncio.create_task(asyncio.run(take_image()))
    imagefilename = str(i) + filename
    imagepath = os.path.join(APP_STATIC, imagefilename)
        
    GPIO.output(laser, True)
    camera.capture('static/'+imagefilename.format(i))
    GPIO.output(laser, False)
    await asyncio.sleep(secondsinterval)
    await task #wait for upload
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)