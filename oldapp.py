#!/usr/bin/env python
from importlib import import_module
import datetime
import time
import subprocess
import os
from flask import Flask, render_template, Response, request, send_file, jsonify
from azure.storage.blob import BlobClient, ContentSettings

connection_string = "DefaultEndpointsProtocol=https;AccountName=soilsamples;AccountKey=Q4mp30h+EtmMzNxZosJEvKaQCpaKG+Y3MF/fITKSwnsTG8Z2/8DbaCnjWwPvDO/tU+zN8VCtTsas+AStNTlxgA==;EndpointSuffix=core.windows.net"
container_name = "soilsensor1"

# import camera driver. Otherwise use pi camera by default
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera_pi import Camera

import utils


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/capture_image', methods=['GET', 'POST'])
def capture_image():
    utils.write_boolean_to_file("camera_state", False)

    filename = request.form.get('filename')
    arguments = request.form.get('arguments')

    cmd = f"raspistill --nopreview -t 1 -o {filename} {arguments}"
    print(cmd)
    
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    print(stdout.decode("utf-8"))
    if process.returncode == 0:
        # upload image to azure blob storage
#         blob_name = filename
#         blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name = blob_name)
#         image_content_setting = ContentSettings(content_type='image/jpeg')
#         with open(filename, "rb") as data:
#             blob.upload_blob(data, overwrite = True, content_settings=image_content_setting)
#             print("Upload complete")
        #return send_file(filename, mimetype='image/jpg')
        return
    else:
        response = {
            "message": "Error capturing image",
            "command": cmd,
            "error": stderr.decode("utf-8")
        }
        return jsonify(response), 500
    
@app.route('/time_lapse', methods=['GET', 'POST'])
def time_lapse():
    utils.write_boolean_to_file("camera_state", False)

    duration_secs = int(request.form.get('duration'))
    num_frames = int(request.form.get('amount'))
    filename = request.form.get('filename')
    arguments = request.form.get('arguments')

    for i in range(num_frames):        
        pic = i + 1
        filename = str(pic)+str(filename)
        cmd = f"raspistill --nopreview -t 1 -o {filename} {arguments}"

        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print("file name " + filename)        
        
        if process.returncode == 0:
            # upload image to azure blob storage
#             blob_name = filename
#             blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name = blob_name)
#             image_content_setting = ContentSettings(content_type='image/jpeg')
#             with open(filename, "rb") as data:
#                 blob.upload_blob(data, overwrite = True, content_settings=image_content_setting)
            print("Upload complete")
        else:
            response = {
                "message": "Error capturing image",
                "command": cmd,
                "error": stderr.decode("utf-8")
            }
            return jsonify(response), 500
        
        time.sleep(duration_secs)
    return


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
