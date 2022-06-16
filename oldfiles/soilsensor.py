import time

import board

from adafruit_seesaw.seesaw import Seesaw

i2c_bus = board.I2C()

ss = Seesaw(i2c_bus, addr = 0x36)

while True:
    touch = ss.moisture_read()
    
    temp = ss.get_temp()
    
    print("temp: " + str(temp) + " moisture: " + str(touch))
    time.sleep(1)
    