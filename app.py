#!/usr/bin/env python
from importlib import import_module
import datetime
import time
import subprocess
import os
import glob
from flask import Flask, render_template, Response, request, json, jsonify

import time_lapse_utils
import hw_utils
import utils
import asyncio
import RPi.GPIO as GPIO
import azure_utils

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

print("IP: " + subprocess.check_output(["hostname -I | cut -d' ' -f1"], shell=True).decode("utf-8"))
      
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera_setting', methods = ['POST', 'GET'])
def camera_setting():
    resolution = eval(request.form.get('resolution'))
    framerate = int(request.form.get('framerate'))
    iso = int(request.form.get('iso'))
    expSpd = int(request.form.get('expSpd'))
    expMod = str(request.form.get('expMod'))
    awbMod = str(request.form.get('awbMod'))
    awbGain = int(request.form.get('awbGain'))
    
    #save camera setting to json file
    CAMERASETTING = {
        "resolution" : resolution,
        "framerate" : framerate,
        "iso" : iso,
        "expSpd" : expSpd,
        "expMod" : expMod,
        "awbMod" : awbMod,
        "awbGain" : awbGain
        }
    with open("CAMERASETTING.json", "w") as file:
        json.dump(CAMERASETTING, file)
    
    # init camera with custom setting
    hw_utils.camera_init()
    
    # capture image (this should be a class called holocam)
    GPIO.output(hw_utils.laser, True)
    try:
        hw_utils.camera.capture('static/preview.jpg')
    except hw_utils.camera.exc.PiCameraMMALError():
        hw_utils.camera_close()
    except hw_tuils.camera.PiCameraClosed:
        hw_utils.camera_init()
        
    GPIO.output(hw_utils.laser, False)
    
    # close camera after time lapse to avoid out of resources error
    hw_utils.camera_close()
    return render_template('index.html', **CAMERASETTING)

@app.route('/start', methods = ['POST', 'GET'])
def start_time_lapse():
    hw_utils.camera_init()
    #set this to the number of minutes you wish to run your timelapse camera
    tlminutes = float(request.form.get('duration'))
    #number of seconds delay between each photo taken
    secondsinterval = int(request.form.get('interval'))
    filename = request.form.get('filename')
    arguments = request.form.get('arguments')
    #number of photos to take
    numphotos = int((tlminutes*60)/secondsinterval) 
    print("number of photos to take = ", numphotos)
    
    dateraw= datetime.datetime.now()
    datetimeformat = dateraw.strftime("%m-%d_%H:%M")
    
    s = time.perf_counter()
    asyncio.run(time_lapse_utils.run(numphotos, secondsinterval, filename))
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
    
    #upload txt file to azure blob
    azure_utils.upload_to_azure_blob("CameraState.txt")
    templateData ={
        'startTime' : datetimeformat,
        'elapseTime' : elapsed,
        'numphotos' : numphotos
        }
    
    return render_template('index.html', **templateData)
    
@app.route('/image_preview')
def image_preview():
    def generate():
        newest = max(glob.iglob('static/*.jpg'), key = os.path.getctime)
        #print(newest)
        yield (b'--frame\r\n' 
          b'Content-Type: image/jpeg\r\n\r\n' + open(newest, 'rb').read() + b'\r\n')
    return Response(generate(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)

