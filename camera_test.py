import time

from picamera2 import Picamera2, Preview

def preview():
    picam2 = Picamera2()
    picam2.start()

    metadata = picam2.capture_file("static/test.jpg")
    print(metadata)

    picam2.close()
