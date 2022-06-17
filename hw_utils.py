import picamera
import RPi.GPIO as GPIO
import time
import board
from adafruit_seesaw.seesaw import Seesaw


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
    GPIO.output(laser, True)
    camera = picamera.PiCamera()
    #with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
#     camera.framerate = 30
#     camera.iso =  50 
    # Wait for automatic gain control to settle
    time.sleep(2)
    GPIO.output(laser, False)
#     # Fix the values
#     camera.shutter_speed = camera.exposure_speed
#     camera.exposure_mode = 'off'
#     #set constant gain
#     g = camera.awb_gains
#     camera.awb_mode = "off"
#     camera.awb_gains = g
    return

def camera_close():
    camera.close()
    return

def soil_sensor_init():
    i2c_bus = board.I2C()
    global soilsensor
    soilsensor = Seesaw(i2c_bus, addr = 0x36)
    return