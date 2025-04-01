"""
TO DO:
Add hotspot for setup with constant IP and still connect to wifi
Add display for checking status
Add dropbox for image upload
"""

#!/usr/bin/env python
from importlib import import_module
import datetime
import time
import glob
import os
from flask import Flask, render_template, Response, request, json, jsonify, send_from_directory, redirect, url_for

# import time_lapse_utils
from camera_utils import preview, time_lapse
import asyncio
import RPi.GPIO as GPIO
from bme68x_utils import get_single_data, start_env_logging_thread

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# set file directory
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')
app.config['UPLOAD_FOLDER'] = APP_STATIC

@app.route('/', methods = ['POST', 'GET'])
def index():
    # setup the hardware sensor & checking on the status
    sensor_data = get_single_data()
    temp = sensor_data["temperature"] if sensor_data else "N/A"
    humidity = sensor_data["humidity"] if sensor_data else "N/A"
    pressure = sensor_data["pressure"] if sensor_data else "N/A"

    if request.method =='POST':
        if request.form['reset_i2c'] == 'Reset I2C':
            sensor_data = get_single_data()
            temp = sensor_data["temperature"] if sensor_data else "N/A"
            humidity = sensor_data["humidity"] if sensor_data else "N/A"
            pressure = sensor_data["pressure"] if sensor_data else "N/A"

    #update flask UI 
    templateData ={
        'temp' : temp,
        'humidity' : humidity,
        'pressure' : pressure,
        }
    
    return render_template('index.html', **templateData)

@app.route('/camera_setting', methods = ['POST', 'GET'])
def camera_setting():
    # grab value from user input on server
    try:
        resolution = eval(request.form.get('resolution'))
        framerate = int(request.form.get('framerate'))
        iso = int(request.form.get('iso'))
        expSpd = int(request.form.get('expSpd'))
        expMod = str(request.form.get('expMod'))
        awbMod = str(request.form.get('awbMod'))
        awbGain = int(request.form.get('awbGain'))
    except SyntaxError as err:
        print(err)
        print("Invalid input. Default value entered")
        resolution = (640, 640)
        framerate = 30
        iso = 60
        expSpd = 2000
        expMod = "off"
        awbMod = "off"
        awbGain = 1
        
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
    
    preview()

    return render_template('index.html', **CAMERASETTING)

@app.route('/start', methods = ['POST', 'GET'])
def start_time_lapse():
    #set this to the number of minutes you wish to run your timelapse camera
    duration_seconds = float(request.form.get('duration'))

    #number of seconds delay between each photo taken
    interval_seconds = int(request.form.get('interval'))
    filename = request.form.get('filename')
    arguments = request.form.get('arguments')

    #number of photos to take
    numphotos = int(duration_seconds/interval_seconds) 
    print("number of photos to take = ", numphotos)
    
    #Record time started for Flask UI
    dateraw= datetime.datetime.now()
    datetimeformat = dateraw.strftime("%m-%d_%H:%M")
    
    #Start time-lapse
    s = time.perf_counter()
    time_lapse(duration_seconds, interval_seconds, filename)
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
    
    #update flask UI 
    templateData ={
        'elapseTime' : elapsed,
        'startTime' : datetimeformat,
        'numphotos' : numphotos
        }
    
    return render_template('index.html', **templateData)

@app.route('/startEnvSensor', methods = ['POST', 'GET'])
def startEnvSensor():
    #number of seconds delay between each photo taken
    interval = int(request.form.get('sensor_interval'))
    duration = float(request.form.get('sensor_duration'))

    start_env_logging_thread(interval, duration)

    return render_template('index.html')

@app.route('/image_preview')
def image_preview():
    def generate():
        # newest = max(glob.iglob('static/*.jpg'), key = os.path.getctime)
        newest = 'static/preview.jpg'
        #print(newest)
        yield (b'--frame\r\n' 
          b'Content-Type: image/jpeg\r\n\r\n' + open(newest, 'rb').read() + b'\r\n')
    return Response(generate(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/image_list')
def image_list():
    # List the image files in the folder (filter if needed)
    images = [f for f in os.listdir(APP_STATIC) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'dng', 'txt'))]
    return render_template('index.html', images=images)

# Route to get the updated list of images (AJAX request)
@app.route('/get_images')
def get_images():
    images = [f for f in os.listdir(APP_STATIC) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'dng', 'txt'))]
    return jsonify(images)

# Route to serve an image file for download
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(APP_STATIC, filename, as_attachment=True)

# Route to delete an image
@app.route('/delete-image/<filename>', methods=['DELETE'])
def delete_image(filename):
    try:
        # Path to your images directory
        image_path = os.path.join(APP_STATIC, filename)
        
        if os.path.exists(image_path):
            os.remove(image_path)
            return jsonify({'message': f'{filename} deleted successfully'}), 200
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)


