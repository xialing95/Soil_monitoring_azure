import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789  # pylint: disable=unused-import

class Display:
    def __init__(self, x=0, width=135, height=240):
        self.x = x
        self.width = width
        self.height = height
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        self.hw_init()   
    
    # init betfore using the display, already called with the object is created
    def hw_init(self):
        # Configuration for CS and DC pins (these are PiTFT defaults):
        cs_pin = digitalio.DigitalInOut(board.CE0)
        dc_pin = digitalio.DigitalInOut(board.D25)
        reset_pin = digitalio.DigitalInOut(board.D24)
        # Turn on the Backlight
        backlight = digitalio.DigitalInOut(board.D23)
        backlight.switch_to_output()
        backlight.value = True
        # Config for display baudrate (default max is 24mhz):
        BAUDRATE = 24000000

        # Setup SPI bus using hardware SPI:
        spi = board.SPI()
        
        self.disp = st7789.ST7789(spi,
                                  rotation=90,
                                  width = self.width,
                                  height = self.height,
                                  x_offset=53,
                                  y_offset=40, # 1.14" ST7789
                                  cs=cs_pin,
                                  dc=dc_pin,
                                  rst=reset_pin,
                                  baudrate=BAUDRATE)
        #     # Make sure to create image with mode 'RGB' for full color.
        if self.disp.rotation % 180 == 90:
            self.height = self.disp.width  # we swap height/width to rotate it to landscape!
            self.width = self.disp.height
        else:
            self.width = self.disp.width  # we swap height/width to rotate it to landscape!
            self.height = self.disp.height
        
        self.image = Image.new("RGB", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
    
    # clears the screen by coloring it with all black
    def clear(self):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=(0, 0, 0))
        self.disp.image(self.image)
    
    # writes text on the screen, the line num starts with 0
    def text(self, text: str, linenum: int):
        # position the text, font set at 12
        self.y = -2 * linenum*-12
        # clear any previous text
        self.draw.rectangle((0, 24*linenum, self.width, 24*(linenum+1)), outline = 0, fill=(0, 0, 0))
        # write the text
        self.draw.text((self.x, self.y), text, font = self.font, fill = "#FFFFFF")
        self.disp.image(self.image)
    
    #def off(self):
        
