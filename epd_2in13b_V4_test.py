#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import epd2in13b_V4
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

import socket
import subprocess

def get_ip_address():
    try:
        # Connect to an external host to force the system to use the default interface
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google's DNS
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return f"Error: {e}"

def get_wifi_name():
    try:
        # Uses iwgetid to get the current WiFi SSID
        result = subprocess.check_output(["iwgetid", "-r"]).decode().strip()
        return result if result else "Not connected to Wi-Fi"
    except subprocess.CalledProcessError:
        return "Wi-Fi interface not found or not connected"

# if __name__ == "__main__":
#     ip = get_ip_address()
#     ssid = get_wifi_name()

#     print(f"IP Address: {ip}")
#     print(f"Wi-Fi SSID: {ssid}")

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in13b_V4 Demo")
    
    epd = epd2in13b_V4.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    time.sleep(1)
    
    # Drawing on the image
    logging.info("Drawing")    
    font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    
    # Drawing on the Horizontal image
    logging.info("1.Drawing on the Horizontal image...") 
    HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 250*122
    HRYimage = Image.new('1', (epd.height, epd.width), 255)  # 250*122
    drawblack = ImageDraw.Draw(HBlackimage)
    drawry = ImageDraw.Draw(HRYimage)
    drawblack.text((10, 0), '10.31.153.230', font = font20, fill = 0)
    drawblack.text((10, 20), '2.13inch e-Paper b V4', font = font20, fill = 0)
    drawblack.text((120, 0), u'微雪电子', font = font20, fill = 0)    
    drawblack.line((20, 50, 70, 100), fill = 0)
    drawblack.line((70, 50, 20, 100), fill = 0)
    drawblack.rectangle((20, 50, 70, 100), outline = 0)    
    drawry.line((165, 50, 165, 100), fill = 0)
    drawry.line((140, 75, 190, 75), fill = 0)
    drawry.arc((140, 50, 190, 100), 0, 360, fill = 0)
    drawry.rectangle((80, 50, 130, 100), fill = 0)
    drawry.chord((85, 55, 125, 95), 0, 360, fill =1)
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
    time.sleep(2)
    
    # logging.info("Clear...")
    # epd.init()
    # epd.clear()
    
    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13b_V4.epdconfig.module_exit(cleanup=True)
    exit()
