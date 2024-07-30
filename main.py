#Trissa
"""
virtua assistant system + augmented reality system for RPi
"""

# imports
import time
import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import subprocess

# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Display Parameters
WIDTH = 128
HEIGHT = 64
BORDER = 5

# Display Refresh
LOOPTIME = 1.0

class OLED_screen:
    def __init__(self):
        # Use for I2C.
        self.i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, self.i2c, addr=0x3C, reset=oled_reset)

        # Clear display.
        self.oled.fill(0)
        self.oled.show()

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        self.width = self.oled.width
        self.height = self.oled.height
        self.image = Image.new('1', (self.width, self.height))

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        # Draw some shapes.
        # First define some constants to allow easy resizing of shapes.
        self.padding = -2
        self.top = self.padding
        self.bottom = self.height - self.padding
        # Move left to right keeping track of the current x position for drawing shapes.
        self.x = 0

        # Load default font.
        self.font = ImageFont.load_default()

        # Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
        # Some other nice fonts to try: http://www.dafont.com/bitmap.php
        # Icons website: https://icons8.com/line-awesome
        self.font = ImageFont.truetype('PixelOperator.ttf', 16)
        self.icon_font = ImageFont.truetype('lineawesome-webfont.ttf', 18)

    def info(self):
        while True:
            # Draw a black filled box to clear the image.
            draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

            # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
            cmd = "hostname -I | cut -d\' \' -f1 | head --bytes -1"
            IP = subprocess.check_output(cmd, shell=True)

            cmd = "top -bn1 | grep load | awk '{printf \"%.2fLA\", $(NF-2)}'"
            CPU = subprocess.check_output(cmd, shell=True)

            cmd = "free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'"
            MemUsage = subprocess.check_output(cmd, shell=True)

            cmd = "df -h | awk '$NF==\"/\"{printf \"HDD: %d/%dGB %s\", $3,$2,$5}'"
            cmd = "df -h | awk '$NF==\"/\"{printf \"%d/%dGB\", $3,$2}'"
            Disk = subprocess.check_output(cmd, shell=True)

            cmd = "vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1"
            Temperature = subprocess.check_output(cmd, shell=True)

            # Icons
            # Icon temperature
            draw.text((self.x, self.top + 5), chr(62609), font=self.icon_font, fill=255)
            # Icon memory
            draw.text((self.x + 65, self.top + 5), chr(62776), font=self.icon_font, fill=255)
            # Icon disk
            draw.text((self.x, self.top + 25), chr(63426), font=self.icon_font, fill=255)
            # Icon cpu
            draw.text((self.x + 65, self.top + 25), chr(62171), font=self.icon_font, fill=255)
            # Icon wifi
            draw.text((self.x, self.top + 45), chr(61931), font=self.icon_font, fill=255)

            # Text
            # Text temperature
            draw.text((self.x + 19, self.top + 5), str(Temperature, 'utf-8'), font=self.font, fill=255)
            # Text memory usage
            draw.text((self.x + 87, self.top + 5), str(MemUsage, 'utf-8'), font=self.font, fill=255)
            # Text Disk usage
            draw.text((self.x + 19, self.top + 25), str(Disk, 'utf-8'), font=self.font, fill=255)
            # Text cpu usage
            draw.text((self.x + 87, self.top + 25), str(CPU, 'utf-8'), font=self.font, fill=255)
            # Text IP address
            draw.text((self.x + 19, self.top + 45), str(IP, 'utf-8'), font=self.font, fill=255)

            # Display image.
            self.oled.image(self.image)
            self.oled.show()
            time.sleep(LOOPTIME)


draw = OLED_screen
