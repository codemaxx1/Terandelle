'''

'''

# imports
import feedparser               # for news RSS
import re                       # used for regular expressions
import wikipedia                # used in searching wikipedia data
import datetime                 # used in time function
import psutil
import requests                 # used to send data requests
import json
import subprocess
import sys


class ExecuteClass:

    def __init__(self, Terandelle):
        self.Terandelle = Terandelle


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
        print(newsArray)

        return 1




    def weather(self, city, Display):
        print(f"city is ... {city}")
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
            self.Terandelle.say(f"i'm sorry, but {city} does not seem to exist.")
            return 0

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

        # build TTS response
        print("creating tts response")
        response = "In " + str(city) + "the weather is " + str(self.weather.weatherDescription) + " and it is " + str(
            round(self.weather.temperature ) ) + " degrees"
        if self.weather.windSpeed > 10:
            response += " and wind speed is " + str(self.weather.windSpeed) + " so it feels like " + str(selfweather.feelsLike)
        # Temperature (in kelvin unit) = " + str(temperature) + " atmospheric pressure (in hPa unit) = " + str(pressure) + " humidity (in percentage) = " + str(humidity) + " description = " +

        Display.printText(f"weather : {self.weather.weatherDescription}", 0, 0, 255)
        Display.printText(f"temp : {self.weather.temperature}", 0, "1textHeight", 255)

        self.Terandelle.say(response)

        return 1



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

        self.say("update of python3 packages complete. Updating text processing datasets and models")
        TextProsessing.update()

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

