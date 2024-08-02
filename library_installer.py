import sys
import subprocess

packages = ["math",
            "time",
            "Adafruit-SSD1306",
            "pillow",
            "feedparser",
            "threading",
            "re",
            "wikipedia",
            "datetime",
            "sys",
            "psutil",
            "requests",
            "json",
            "socket",
            "SpeechRecognition",
            "spacy",
            "gTTS",
            "python-vlc"
]

print("installing packages")
for package in packages:
    print(f"installing {package}")
    # implement pip3 as a subprocess:
    subprocess.check_call([sys.executable, '-m', 'pip3', 'install', package])

    # process output with an API in the subprocess module:
    reqs = subprocess.check_output([sys.executable, '-m', 'pip3', 'freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    print(installed_packages)

print("done installing packages")

