import sys
import subprocess

packages = [#"math",
            #"time",
            ["pip3", "install", "Adafruit-SSD1306"],
            ["pip3", "install", "pillow"],
            ["pip3", "install", "feedparser"],
            #["pip3", "install", "threading"],
            #["pip3", "install", "re"],
            ["pip3", "install", "wikipedia"],
            ["pip3", "install", "datetime"],
            ["pip3", "install", "sys"],
            ["pip3", "install", "psutil"],
            ["pip3", "install", "requests"],
            ["pip3", "install", "json"],
            ["pip3", "install", "RPi.GPIO"],
            ["pip3", "install", "socket"],
            ["pip3", "install", "PyAudio"],
            ["pip3", "install", "SpeechRecognition"],
            ["pip3", "install", "spacy"],
            ["pip3", "install", "gTTS"],
            ["pip3", "install", "python-vlc"],
        ]

print("installing packages")
for package in packages:
    print(f"installing {package}")
    # implement pip3 as a subprocess:
    try:
        subprocess.check_call([package])

        # process output with an API in the subprocess module:
        reqs = subprocess.check_output([sys.executable, '-m', 'pip3', 'freeze'])
        installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
        print(installed_packages)
    except Exception as e:
        print("falure in installing {0} because of {1}".format(package, e))

print("done installing packages")

