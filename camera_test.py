import time

from picamera2 import Picamera2, Preview

picam2 = Picamera2()
picam2.start()
time.sleep(2)

metadata = picam2.capture_file("test.jpg")
print(metadata)

picam2.close()