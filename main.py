# Terandelle
"""

"""

#imports

import math
import time
import adafruit_ssd1306         # for OLED interface
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import feedparser               # for news RSS
import threading
import re                       # used for regular expressions
import wikipedia                # used in searching wikipedia data
import subprocess
import datetime                 # used in time function
import sys
import psutil
import requests                 # used to send data requests
import json
import socket                   # for determining IP
import speech_recognition as sr # for speech recognition
#import spacy                    # for natural language processing
from gtts import gTTS           # for tts
import vlc
#from playsound import playsound # to play TTS .mp3 file after it is generated
import board                        #for screen

'''
    Person class, for use with loading data on peoplpe
'''
class Person:
    def __init__(self, personData):
        self.firstName = personData.firstName
        self.lastName = personData.lastName
        self.birthday = personData.birthday
        self.pronouns = personData.pronouns


'''
    Terandelle class
    for main functionality of the Terandelle system
'''
class Terandelle:
    # user, for use in identifying authority and for customizing response data
    user = "guest"

    def __init__(self, Display):
        self.Display = Display
        subprocess.run(["pulseaudio", "-D"])


    def speakingThread(self, text):
        '''
        use google tts to convert text into an mp3 file, then use playsound to play that file
        :param text: the text to speak
        :return: the text that was spoken
        '''
        tts = gTTS(text, lang='en')
        # Save converted audio as mp3 format
        tts.save('ttsOut.mp3')

        p = vlc.MediaPlayer("ttsOut.mp3")
        p.play()
        return text


    def say(self, words):
        '''
        create a thread to speak the words
        :param words: the words to be spoken
        :return: the thread info after it was started
        '''
        print(f"speaking (via tts) \"{words}\"")
        thread = threading.Thread(target=self.speakingThread, args=(words,), daemon=True)
        thread.start()
        return thread


    def login(self):
        '''
        login user
        :return: user
        '''
        user = "Ira"
        return user


    def getBatteryInformation(self):
        '''
        get the battery information for the system
        :return: battery info
        '''
        # get battery data
        batteryInfo = psutil.sensors_battery()
        # print("Battery percentage : ", battery.percent)
        # print("Power plugged in : ", battery.power_plugged)
        # converting seconds to hh:mm:ss
        # print("Battery left : ", convertTime(battery.secsleft))
        return batteryInfo


    def update(self):
        '''
        update Terandelle program from git repo
        :return: return of subprocess call for update
        '''
        #self.say("pulling from remote repo")

        returnedValue = [0,0]
        returnedValue[0] = subprocess.check_output(["git", "pull"])

        #self.say(returnedValue.decode("utf-8"))

        self.say("update of program complete. Now, I'm updating Python3 packages")

        updatePackages = "python3 library_installer.py"
        returnedValue[1] = subprocess.call(str(updatePackages), shell=True)

        return returnedValue


    def restartProgram(self):
        '''
        restart program by creating a new instance of it and terminating this one
        :return: none
        '''
        self.say("restarting program")
        openNewProcess = "python3 " + str(sys.argv[0])
        subprocess.call(str(openNewProcess), shell=True)    # open new instance of self
        sys.exit()                                          # terminate instance of self


    def getDateTime(self):
        '''
        return the current datetime data in the requested format
        :return: datetime data
        '''
        now = datetime.datetime.now()
        dateTimeData = {"second":now.second,
                        "minute" : now.minute,
                        "hour" : now.hour,
                        "day" : now.day,
                        "month" : now.month,
                        "year" : now.year,
                        }

        return dateTimeData


    def wikipediaDefine(self, query, lineStart, lineEnd):
        '''
        parse the first bit of the wikipedia article about input:query
        :param query: the thing you want to know about
        :param lineStart: the position in the text that you want to start reading from (typically zero)
        :param lineEnd: the position in the text that you want to stop reading at
        :return:
        '''
        self.say("let's see what I can find")
        try:
            text = wikipedia.summary(str(query))
            defineTextList = text.split('.')

            # loop through input:lines, or fewer lines in the return if there are fewer than input:lines lines in it
            for i in range( lineStart, min(len(defineTextList) + 1, lineEnd) ):
                print("line: " + str(i))
                self.say(defineTextList[i])
        except Exception as e:
            self.say(f"failure finding information about {query} because of {e}, could you try again?")


    def getNews(self):
        '''
        parse the yahoo news rss feed for information about the world today
        :return: newsfeed data
        '''
        d = feedparser.parse('https://www.yahoo.com/news/rss')
        newsFeedList = []
        for post in d.entries:
            newsFeedList.append(post.title)
        return newsFeedList


    def news(self, Display):
        '''
        get you your news
        :return: 1 on completion
        '''
        newsArray = self.getNews()


        return 1


    def getWeather(self, city):
        '''
        return the weather data for a specific city
        :param city: the name of a city
        :return: 1 on success
        '''
        apiKey = '75f6c15e22433ed3e7406b24691a0706'                         # api key (might be outdated)
        baseURL = "http://api.openweathermap.org/data/2.5/weather?"         # url to get data from
        url = baseURL + "appid=" + apiKey + "&q=" + city

        # send data request and get JSON
        requestResponse = requests.get(url)
        jsonResponse = requestResponse.json()
        print(jsonResponse)
        # if city is found
        if jsonResponse["cod"] != "404":

            # define weather variables
            self.temperature = jsonResponse["main"]["temp"]
            self.pressure = jsonResponse["main"]["pressure"]
            self.humidity = jsonResponse["main"]["humidity"]
            self.feelsLike = jsonResponse["main"]["feels_like"]
            self.tempMin = jsonResponse["main"]['temp_min']
            self.tempMax = jsonResponse["main"]['temp_max']
            self.coordinates = jsonResponse['coord']
            self.visibility = jsonResponse['visibility']
            self.windSpeed = jsonResponse['wind']['speed']
            self.windDirection = jsonResponse['wind']['deg']
            self.clouds = jsonResponse['clouds']
            self.name = jsonResponse['name']
            self.weather = jsonResponse["weather"]
            self.weatherDescription = self.weather[0]["description"]
            self.main = self.weather[0]['main']

            # convert units from kelvin to Farenheight
            self.temperature = (9 / 5) * (self.temperature - 273) + 32

        else:
            self.say(f"i'm sorry, but {city} does not seem to exist.")

            """
            example of returned weather JSON
            {   'coord': {'lon': -111.7897, 'lat': 43.826}, 
                'weather': [{
                    'id': 801, 
                    'main': 'Clouds', 
                    'description': 'few clouds', 
                    'icon': '02n'}], 
                'base': 'stations', 
                'main': {
                    'temp': 263.05, 
                    'feels_like': 258.83, 
                    'temp_min': 261.88, 
                    'temp_max': 274.74, 
                    'pressure': 1011, 
                    'humidity': 79}, 
                'visibility': 10000, 
                'wind': {'speed': 2.06, 'deg': 50}, 
                'clouds': {'all': 20}, 
                'dt': 1641263617, 
                'sys': {
                    'type': 1, 
                    'id': 5735, 
                    'country': 'US', 
                    'sunrise': 1641222077, 
                    'sunset': 1641254509}, 
                'timezone': -25200, 
                'id': 5605242, 
                'name': 'Rexburg', 
                'cod': 200}
            """
        return 1


    def weather(self, city, Display):
        weather = self.getWeather(city)
        # build TTS response
        response = "In " + str(city) + "the weather is " + str(weather.weatherDescription) + " and it is " + str(
            round(weather.temperature ) ) + " degrees"
        if weather.windSpeed > 10:
            response += " and wind speed is " + str(weather.windSpeed) + " so it feels like " + str(weather.feelsLike)
        # Temperature (in kelvin unit) = " + str(temperature) + " atmospheric pressure (in hPa unit) = " + str(pressure) + " humidity (in percentage) = " + str(humidity) + " description = " +

        Display.printText(f"weather : {weather.weatherDescription}", 0, 0, 255)
        Display.printText(f"temp : {weather.temperature}", 0, "1textHeight", 255)

        self.say(response)

        return 1


    def bootup(self, Display):
        '''
        perform some functions at time of startup
        :param display: instance of the display class, named display
        :return: 1 on success
        '''
        self.say("Terandelle system, booting up")
        Display.bootup()
        self.user = self.login()
        self.say("Ready for your command")

        return 1


    def listen(self, Display):
        '''
        listen to audio input from the attached microphone and run it through the speech recognition server
        :param display: instance of display class
        :return: the text-converted voice data
        '''
        r = sr.Recognizer()
        wordsSpoken = ""
        with sr.Microphone() as source:
            print('Say something...')
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
        try:
            wordsSpoken = r.recognize_google(audio).lower()
            print('You said: ' + wordsSpoken + '\n')
        # loop back to continue to listen for commands if unrecognizable speech is received
        except sr.UnknownValueError:
            print('unknown error')
        return str(wordsSpoken)


    def perform(self, command, Display):
        '''
        take the words spoken data from the listen() function and actually run a command from it
        :param command: the text of words spoken
        :param display: class instance of display
        :return: the name of the function run
        '''
        command = command.lower()

        functionRun = command

        Display.printText(command, 0, 0, 255)
        Display.updateScreen()

        return functionRun


"""
    display class
    for functionality relating to the display
"""
class Display:
    def __init__(self):
        self.displayHeight = 128
        self.displayWidth = 64

        i2c = board.I2C()
        self.disp = adafruit_ssd1306.SSD1306_I2C(self.displayWidth, self.displayHeight, i2c)
        # Clear display.
        self.disp.fill(0)
        self.disp.show()

        self.image = Image.new("1", (self.displayWidth, self.displayHeight))
        self.font = ImageFont.load_default()
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

        text = "Terandelle"
        self.printText(self.displayWidth / 2, self.displayHeight / 2, text, fill=1)
        text = "Booting up"
        self.printText(self.displayWidth / 2, self.displayHeight / 2, text, fill=1)
        self.printText(0, 0, IP, fill=1)

        # perform visual loop for displayWidth frames
        for i in range(self.displayWidth):

            for j in range(self.displayHeight):
                self.draw.rectangle((i, j, i+1, j+1), outline=255, fill=0)
                #self.oled.pixel(i, j, 1)

                self.updateScreen()
                time.sleep(0.01)



            #self.draw.line((self.width/2-radius + x, self.height/2-radius + y, self.width/2, self.height/2), fill=0)

            # update screen
            #self.display.image(self.image)
            #self.display.show()

            # refresh rate
            #time.sleep(0.05)
        print("bootup done")
        return 1


    def printText(self, x, y, text, fill):
        '''
        print text
        :param text: (str)
        :param x: x position of text
        :param y:  y position of text
        :param fill:  0 to not fill or 1 to fill
        :return:
        '''
        self.draw.text((x, y), text, font=self.font, fill=fill)

    def updateScreen(self):
        # update screen
        self.disp.image(self.image)
        self.disp.show()


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

if __name__ == "__main__":
    print("init display")
    Display = Display()

    print("init terandelle")
    Terandelle = Terandelle(Display)

    time.sleep(1)

    #print("update")
    #Terandelle.update()

    time.sleep(2)

    print("bootup sequence")
    Terandelle.bootup(Display)

    Terandelle.perform(Terandelle.listen(Display), Display)

    print("display wave")
    Display.wave()