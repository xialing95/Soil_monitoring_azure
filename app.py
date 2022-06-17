#!/usr/bin/env python
from importlib import import_module
import datetime
import time
import subprocess
import os
import glob
from flask import Flask, render_template, Response, request, send_file, jsonify

import time_lapse_app
import utils
import asyncio

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera_setting', methods = ['POST', 'GET'])
def camera_setting():
    return

@app.route('/start', methods = ['POST', 'GET'])
def start_time_lapse():
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
    print("RPi started taking photos for your timelapse at: " + datetimeformat)
    
    s = time.perf_counter()
    asyncio.run(time_lapse_app.run(numphotos, secondsinterval, filename))
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
    
    templateData ={
        'state' : 'Done',
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

@app.route('/file_setting', methods=['GET', 'POST'])
def file_setting():
    #set this to the number of minutes you wish to run your timelapse camera
    tlminutes = float(request.form.get('duration'))
    #number of seconds delay between each photo taken
    secondsinterval = int(request.form.get('interval'))
    filename = request.form.get('filename')
    arguments = request.form.get('arguments')
    #number of photos to take
    numphotos = int((tlminutes*60)/secondsinterval) 
    print("number of photos to take = ", numphotos)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)
