import picamera
import RPi.GPIO as GPIO
import time
import board
from adafruit_seesaw.seesaw import Seesaw
import json


### Light and Camera Setup ###
def light_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    global laser
    laser = 17 #GPIO17, pin 11
    bottonSts = GPIO.LOW
    GPIO.setup(laser, GPIO.OUT)
    return

def camera_init(): 
    global camera
    light_init()
    with open("CAMERASETTING.json") as file:
        data = json.load(file)
        
    GPIO.output(laser, True)
    camera = picamera.PiCamera()
    #with picamera.PiCamera() as camera:
    camera.resolution = data["resolution"]
    camera.framerate = data["framerate"]
    camera.iso = data["iso"]
    # Wait for automatic gain control to settle
    time.sleep(2)
    GPIO.output(laser, False)
    camera.shutter_speed = data["expSpd"]
    camera.exposure_mode = data["expMod"]
    camera.awb_mode = data["awbMod"]
    camera.awb_gains = data["awbGain"]
    return

def camera_close():
    camera.close()
    return

def soil_sensor_init():
    i2c_bus = board.I2C()
    global soilsensor
    soilsensor = Seesaw(i2c_bus, addr = 0x36)
    return