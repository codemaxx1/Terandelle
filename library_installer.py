import sys
import subprocess

packages = [#"math",
            #"time",
            #["pip3", "install", "Adafruit-SSD1306"],
            #["pip3", "install", "adafruit-circuitpython-ssd1306"],
            ["pip3", "install", "board"],
            ["pip3", "install", "I2CDisplayBus"],
            ["pip3", "install", "displayio"],
            ["pip3", "install", "terminalio"],
            ["pip3", "install", "adafruit-circuitpython-displayio-ssd1306"],
            ["pip", "install", "adafruit-blinka-displayio"],
            ["pip", "install", "adafruit-circuitpython-display-text"],
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
            ["pip3", "install", "RPi.GPIO"],
            ["pip3", "install", "nltk", "spacy"],
            ["python3", "-m", "spacy", "download", "en_core_web_sm"],
            ["pip3", "install", "socket"],
            ['sudo', "apt-get", "install", "portaudio19-dev", "python-pyaudio", "-y"],
            ["sudo", "apt-get", "install", "flac"]
            ["pip3", "install", "PyAudio"],
            ['pip3', 'install', 'pipwin'],
            ["pipwin", 'install', 'pyaudio']
            ["pip3", "install", "SpeechRecognition"],
            ["pip3", "install", "spacy"],
            ["pip3", "install", "gTTS"],
            ["pip3", "install", "python-vlc"],
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
    except Exception as e:
        print("falure in installing {0} because of {1}".format(package, e))
        failureList.append(package)

print('failed packages: {0}'.format(failureList))
print("done installing packages")

