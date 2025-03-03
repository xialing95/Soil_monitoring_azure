#!/usr/bin/env python
from importlib import import_module
import datetime
import time
import glob
from flask import Flask, render_template, Response, request, json, jsonify

# import time_lapse_utils
from camera_utils import preview, time_lapse
import asyncio
import RPi.GPIO as GPIO
from bme68x_utils import BME680Sensor

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/', methods = ['POST', 'GET'])
def index():
    # setup the hardware sensor & checking on the status
    sensor = BME680Sensor()   # Initialize the sensor

    sensor_data = sensor.read_sensor_data()  # Read sensor data
    temp = sensor_data["temperature"] if sensor_data else "N/A"
    humidity = sensor_data["humidity"] if sensor_data else "N/A"
    sensor.print_sensor_data()

    if request.method =='POST':
        if request.form['reset_i2c'] == 'Reset I2C':
            sensor = BME680Sensor()  # Initialize the sensor

            sensor_data = sensor.read_sensor_data()  # Read sensor data
            temp = sensor_data["temperature"] if sensor_data else "N/A"
            humidity = sensor_data["humidity"] if sensor_data else "N/A"
            sensor.print_sensor_data()

    #update flask UI 
    templateData ={
        'temp' : temp,
        'humidity' : humidity,
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
    tlminutes = float(request.form.get('duration'))
    #number of seconds delay between each photo taken
    secondsinterval = int(request.form.get('interval'))
    filename = request.form.get('filename')
    arguments = request.form.get('arguments')
    #number of photos to take
    numphotos = int((tlminutes*60)/secondsinterval) 
    print("number of photos to take = ", numphotos)
    
    #Record time started for Flask UI
    dateraw= datetime.datetime.now()
    datetimeformat = dateraw.strftime("%m-%d_%H:%M")
    
    #Start time-lapse
    s = time.perf_counter()
    time_lapse(tlminutes, secondsinterval, filename)
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
    
    #update flask UI 
    templateData ={
        'elapseTime' : elapsed,
        'startTime' : datetimeformat,
        'numphotos' : numphotos
        }
    
    return render_template('index.html', **templateData)
    
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)


