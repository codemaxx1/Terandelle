'''
displayClass contains the class Display, whose entire purpose in life is to work with the OLED display
'''


# imports
import board                        #for screen
import pygame                       # for high resolution sleep/delay function
import math
import time
from random import randrange
import socket                   # for determining IP
import adafruit_ssd1306         # for OLED interface
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import busio

"""
    display class
    for functionality relating to the display
"""
class Display:
    def __init__(self, displayWidth, displayHeight):
        self.displayHeight = displayHeight
        self.displayWidth = displayWidth

        i2c = busio.I2C(board.SCL, board.SDA)
        self.oled = adafruit_ssd1306.SSD1306_I2C(self.displayWidth, self.displayHeight, i2c)

        self.clearScreen()

        self.image = Image.new("1", (self.displayWidth, self.displayHeight))

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)


    def bootup(self):
        '''
        graphical sequence for the bootup operation
        :return: 1 on successful completion
        '''

        # IP address
        try:
            IP = socket.gethostbyname(socket.gethostname())
        except:
            IP = "network unreachable"

        # perform visual loop for displayWidth frames
        for i in range(round(self.displayWidth/3)):

            for j in range(round(self.displayHeight/2)):
                x = randrange(0, self.displayWidth)
                y = randrange(0, self.displayHeight)
                self.draw.rectangle((x, y, x+1, y+1), outline=255, fill=0)

                text = "Terandelle"
                self.printText(self.displayWidth / 2, self.displayHeight / 2, text, 1)
                text = "Booting up"
                self.printText(self.displayWidth / 2, self.displayHeight / 2 + 20, text, 1)
                self.printText(0, 0, IP, 1)

                self.updateScreen()
                pygame.time.wait(1)  # Milliseconds

            #self.draw.line((self.width/2-radius + x, self.height/2-radius + y, self.width/2, self.height/2), fill=0)
        self.clearScreen()
        print("bootup done")
        return 1


    def clearScreen(self):
        '''
        as the name implies, this method is the clear the display
        :return:
        '''
        # Clear display.
        self.oled.fill(0)
        self.updateScreen()

    def printText(self, x, y, text, fill):
        '''
        print text
        :param text: (str)
        :param x: x position of text
        :param y:  y position of text
        :param fill:  0 to not fill or 1 to fill
        :return:
        '''
        # Load default font.
        font = ImageFont.load_default()

        # Draw Some Text
        self.draw.text((x, y), text, font=font, fill=fill)


    def updateScreen(self):
        '''
        update the screen with the new image draw data
        :return:
        '''
        # update screen
        self.oled.image(self.image)
        self.oled.show()


    def wave(self):
        return 0
    '''
    def wave(self):

        # Define text and get total width.
        text = 'SSD1306 ORGANIC LED DISPLAY. THIS IS AN OLD SCHOOL DEMO SCROLLER!! GREETZ TO: LADYADA & THE ADAFRUIT CREW, TRIXTER, FUTURE CREW, AND FARBRAUSCH'
        maxwidth, unused = self.draw.textsize(text, font=self.font)

        # Set animation and sine wave parameters.
        amplitude = self.height/4
        offset = self.height/2 - 4
        velocity = -2
        startpos = self.width

        # Animate text moving in sine wave.
        print('Press Ctrl-C to quit.')
        pos = startpos
        while True:
            # Clear image buffer by drawing a black filled box.
            self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
            # Enumerate characters and draw them offset vertically based on a sine wave.
            x = pos
            for i, c in enumerate(text):
                # Stop drawing if off the right side of screen.
                if x > self.width:
                    break
                # Calculate width but skip drawing if off the left side of screen.
                if x < -10:
                    char_width, char_height = self.draw.textsize(c, font=self.font)
                    x += char_width
                    continue
                # Calculate offset from sine wave.
                y = offset+math.floor(amplitude*math.sin(x/float(self.width)*2.0*math.pi))
                # Draw text.
                self.draw.text((x, y), c, font=self.font, fill=255)
                # Increment x position based on chacacter width.
                char_width, char_height = self.draw.textsize(c, font=self.font)
                x += char_width
            # Draw the image buffer.
            disp.image(self.image)
            disp.display()
            # Move position for next frame.
            pos += velocity
            # Start over if text has scrolled completely off left side of screen.
            if pos < -maxwidth:
                pos = startpos
            # Pause briefly before drawing next frame.
            time.sleep(0.1)
    '''
