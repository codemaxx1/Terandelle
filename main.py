# Terandelle
"""

"""

#imports
import threading
import subprocess
import sys
import time
import speech_recognition as sr # for speech recognition
from gtts import gTTS           # for tts
import vlc

# custom classes
from displayClass import Display
from personClass import Person
from textProcessingClass import TextProcessing
from executeClass import ExecuteClass

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
            r.pause_threshold = 2
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, phrase_time_limit=5)
        try:
            wordsSpoken = r.recognize_google(audio).lower()
            print('You said: ' + wordsSpoken + '\n')
        # loop back to continue to listen for commands if unrecognizable speech is received
        except sr.UnknownValueError:
            print('unknown error in speech recognition module')
        return str(wordsSpoken)


    def perform(self, Terandelle, Display, TextProcessing):
        '''
        take the words spoken data from the listen() function and actually run a command from it
        :param command: the text of words spoken
        :param display: class instance of display
        :return: the name of the function run
        '''
        while True:
            try:
                # give signal that we are ready for a command
                Display.printText(50, 0, "please speak", 1)
                Display.drawCircle("middle", "middle", 10, 1, 1)
                Display.updateScreen()

                # listen for a command
                command = Terandelle.listen(Display)

                Display.printText(0, 0, f"you said:", 1)
                Display.printText(0, 10, f"\"{command}\"", 1)

                functionRun, properNoun = TextProcessing.recognizeIntent(TextProcessing.analyzeCommand(command))
                functionRun = str(functionRun)
                properNoun = str(properNoun)

                print(f"functionRun={functionRun}, properNoun={properNoun}")

                if functionRun == "update":
                    print("update")
                    Execute.update(Display)
                elif functionRun == "restart":
                    print("restart")
                    Execute.restartProgram()
                elif functionRun == "news":
                    print("news")
                    Execute.news(Display)
                elif functionRun == "time":
                    print("time")
                    Execute.getDateTime()
                elif functionRun == "wikipedia":
                    print("wikipedia")
                    Execute.wikipediaDefine("thing to query", 0, 3)
                elif functionRun == "weather":
                    print("weather")
                    Execute.weather(properNoun, Display)

                # update the image buffer
                Display.updateScreen()
                #time.sleep(1)
            except Exception as e:
                Terandelle.say("Fatal Error. I won't shutdown right now, just be aware that there was a fatal error. Error description: {0}".format(e))
        return functionRun


if __name__ == "__main__":

        displayHeight = 64
        displayWidth = 128


        print("init display")
        Display = Display(displayWidth, displayHeight)

        print("init terandelle")
        Terandelle = Terandelle(Display)


        print('init execute')
        Execute = ExecuteClass(Terandelle)

        #print("update")
        #Terandelle.update()

        print("bootup sequence")
        #Terandelle.bootup(Display)


        print('init text processing')
        TextProcessing = TextProcessing()

        # begin performing functions
        Terandelle.perform(Terandelle, Display, TextProcessing)

        print("display wave")
        Display.wave()

