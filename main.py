# Terandelle
"""

"""

#imports

# for screen
import math
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import threading
# for tts
from gtts import gTTS
from playsound import playsound

# Raspberry Pi pin configuration:
RST = 24

# 128x32 display with hardware I2C:
#disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)



# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
class Terandelle:
    def __init__(self, display):
        self.display = display

    def speakingThread(self, text):
        tts = gTTS(text, lang='en')
        # Save converted audio as mp3 format
        tts.save('ttsOut.mp3')
        playsound("ttsOut.mp3")

    def say(self, words):
        thread = threading.Thread(target=self.speakingThread, args=(words,), daemon=True)
        thread.start()

    def bootup(self, display):
        text = "Terandelle"
        self.say(text)
        display.bootup()




class display:
    def __init__(self):
        # Initialize library.
        disp.begin()

        # Get display width and height.
        self.width = disp.width
        self.height = disp.height

        # Clear display.
        disp.clear()
        disp.display()

        # Create image buffer.
        # Make sure to create image with mode '1' for 1-bit color.
        self.image = Image.new('1', (self.width, self.height))

        # Load default font.
        self.font = ImageFont.load_default()

        # Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as this python script!
        # Some nice fonts to try: http://www.dafont.com/bitmap.php
        # font = ImageFont.truetype('Minecraftia.ttf', 8)

        # Create drawing object.
        self.draw = ImageDraw.Draw(self.image)

    def bootup(self):
        # Define text and get total width.
        text = "Terandelle"
        maxwidth, unused = self.draw.textsize(text, font=self.font)

        # Set animation and sine wave parameters.
        amplitude = self.height / 4
        offset = self.height / 2 - 4
        velocity = -2
        startpos = self.width

        # Animate text moving in sine wave.
        pos = startpos
        for i in range(200):
            radius = i/2

            x = (self.width/2) * math.sin(radius)
            y = (self.height/2) * math.cos(radius)
            self.draw.line((self.width/2-radius + x, self.height/2-radius + y, self.width/2, self.height/2), fill=255)

            self.draw.ellipse((self.width/2-radius + x, self.height/2-radius + y, self.width/2+radius + x, self.height/2+radius + y), outline=255, fill=255)
            self.draw.text((self.width / 2, self.height / 2), text, font=self.font, fill=255)
            self.draw.text((0,0), text, font=self.font, fill=255)
            self.draw.text((50,20), text, font=self.font, fill=255)

            disp.image(self.image)
            disp.display()
            time.sleep(0.05)
        print("bootup done")


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

if __name__ == "__main__":
    print("init display")
    display = display()



    print("init terandelle")
    Terandelle = Terandelle(display)

    print("bootup sequence")
    Terandelle.bootup(display )

    print("display wave")
    display.wave()
