import picamera2
import RPi.GPIO as GPIO
import time
# import board
# import busio
# from adafruit_seesaw.seesaw import Seesaw
import json
import subprocess
import signal
import sys

# Holocam class
class Holocam:
    def __init__(self, laserPin = 24):
        self.laserPin = laserPin
        # initalize the laser GPIO & Camera setting
        self.laser_init()
        self.camera_init()
    
    def laser_init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.laserPin, GPIO.OUT)
        
    def laser_on(self):
        GPIO.output(self.laserPin, True)
    
    def laser_off(self):
        GPIO.output(self.laserPin, False)
    
    def camera_init(self):
        # open the camera setting files 
        with open("CAMERASETTING.json") as file:
            data = json.load(file)
            
        self.laser_on
        
        try:
            self.camera = picamera.PiCamera()
        except Exception as e:
            self.camera_close()
            print(e)
        
#         try:
#             self.camera = picamera.PiCamera()
#         except self.camera.PiCameraMMALError:
#             self.camera_close()
        
        try:    
            self.camera.resolution = data["resolution"]
            self.camera.framerate = data["framerate"]
            self.camera.iso = data["iso"]
            # Wait for automatic gain control to settle
            time.sleep(2)
            self.laser_off
            self.camera.shutter_speed = data["expSpd"]
            self.camera.exposure_mode = data["expMod"]
            self.camera.awb_mode = data["awbMod"]
        except SyntaxError as err:
            print (err)
            print("Invalid Camera Setting") 
    
    # camera capture    
    def camera_capture(self, path):
        self.camera.capture(path)
    
    # Holographic image capture    
    def capture(self, path):
        self.laser_on()
        
        try:
            self.camera_capture(path)
        except Exception as e:
            self.camera_close()
            self.camera_init()
            print(e)
            
#         try:
#             self.camera_capture(path)
#         except self.camera.PiCameraMMALError:
#             self.camera_close()
#         except self.camera.PiCameraClosed:
#             self.camera_init()
        
        self.laser_off()
    
    def camera_close(self):
        self.camera.close()

# I2C sensor Class
# class Soilsensor:
#     def __init__(self):
#         self.i2c_bus = board.I2C()
#         self.


# def soil_sensor_init():
#     i2c_bus = board.I2C()
#     global soilsensor
#     try:
#         soilsensor = Seesaw(i2c_bus, addr = 0x36)
#     except ValueError as err:
#         print(err)
#         print("Please connect the I2C Device")
#     return      

def shutdown_callback(channel):
    print("Shutdown Started")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(27, False)
    GPIO.setup(22, GPIO.OUT)
    GPIO.output(22, False)
    GPIO.setup(25, GPIO.OUT)
    GPIO.output(25, False)
    GPIO.cleanup()
    subprocess.call(['sudo shutdown now "System halted by power switch "'], shell=True)

# def signal_handler(sig, frame):
# 
#     sys.exit(0)
    
def shutdown_bnt(shutdownPin):
    print("shutdown pin started")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(shutdownPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    GPIO.add_event_detect(shutdownPin, GPIO.FALLING,
                          callback=shutdown_callback, bouncetime = 2000)

#     signal.signal(signal.SIGINT, signal_handler)
#     signal.pause()

# ### Light and Camera Setup ###
# def light_init():
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setwarnings(False)
    # global laser
    # laser = 17 #GPIO17, pin 11
    # bottonSts = GPIO.LOW
    # GPIO.setup(laser, GPIO.OUT)
    # return

# def camera_init(): 
    # global camera
    # light_init()
    # with open("CAMERASETTING.json") as file:
        # data = json.load(file)
        
    # GPIO.output(laser, True)
    # camera = picamera.PiCamera()
    # #with picamera.PiCamera() as camera:
    # camera.resolution = data["resolution"]
    # camera.framerate = data["framerate"]
    # camera.iso = data["iso"]
    # # Wait for automatic gain control to settle
    # time.sleep(2)
    # GPIO.output(laser, False)
    # camera.shutter_speed = data["expSpd"]
    # camera.exposure_mode = data["expMod"]
    # camera.awb_mode = data["awbMod"]
    # camera.awb_gains = data["awbGain"]
    # return

# def camera_close():
    # camera.close()
    # return    
