import sys
import subprocess
import os

packages = [#"math",
            #"time",
            #["pip3", "install", "Adafruit-SSD1306"],
            ["pip3", "install", "adafruit-circuitpython-ssd1306"],
            ["pip3", "install", "board"],
            #["pip3", "install", "I2CDisplayBus"],

            #["pip3", "install", "displayio"],
            #["pip3", "install", "terminalio"],
            #["pip3", "install", "Adafruit_SSD1306"],
            ["pip3", "install", "pillow"],
            ["pip3", "install", "feedparser"],
            ["pip3", "install", "pygame"],
            #["pip3", "install", "threading"],
            #["pip3", "install", "re"],
            ["pip3", "install", "wikipedia"],
            ["pip3", "install", "datetime"],
            ["pip3", "install", "sys"],
            ["pip3", "install", "psutil"],
            ["pip3", "install", "requests"],
            ["pip3", "install", "json"],
            #["sudo", "apt-get", "install", "libopenblas-dev", " -y"]
            #['pip3', 'install', 'https://github.com/explosion/spacy-models/releases/download/de_core_news_lg-3.1.0/de_core_news_lg-3.1.0-py3-none-any.whl'],
            #["pip3", "install", "RPi.GPIO"],
            ["pip3", "install", "nltk", "spacy"],
            ["python3", "-m", "spacy", "download", "en_core_web_sm"],
            ["pip3", "install", "socket"],
            ["sudo", "apt-get", "install", "alsa-utils"],
            ['sudo', "apt-get", "install", "portaudio19-dev", "python-pyaudio", "-y"],
            ["sudo", "apt-get", "install", "flac"],
            ["pip3", "install", "PyAudio"],
            ['pip3', 'install', 'pipwin'],
            ["pipwin", 'install', 'pyaudio'],
            ["pip3", "install", "SpeechRecognition"],
            ["pip3", "install", "spacy"],
            ["pip3", "install", "gTTS"],
            ["pip3", "install", "python-vlc"],
            ["pip3", "install", "RPi.GPIO"],
        ]

failureList = []
print("installing packages")
for package in packages:
    print(f"installing {package}")
    # implement pip3 as a subprocess:
    try:
        subprocess.check_call(package)

        # process output with an API in the subprocess module:
        reqs = subprocess.check_output([sys.executable, '-m', 'pip3', 'freeze'])
        installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
        print(installed_packages)
    except KeyboardInterrupt:
        quit()
    except:
        installCMD = ''
        for i in range(len(package)):
            installCMD += " " + package[i]

        try:
            if "pip3" not in installCMD:
                os.system(installCMD)
            else:
                print("unable to install python package {0}".format(package[i]))
        except KeyboardInterrupt:
            quit()
        except Exception as e:
            print("double falure in installing {0} because of {1}".format(package, e))
            failureList.append(package)


print('\x1b[1;33m failed packages: {0} \x1b[0m'.format(failureList))
print("done installing packages")

