import pyaudio
import boto3
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
from io import BytesIO
import threading
import time
import wave

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

fileName = "recording.wav"
p = pyaudio.PyAudio()
frames = []

stream = p.open(format=FORMAT,
                channels=CHANNELS, 
                rate=RATE, 
                input=True,
                output=True,
                frames_per_buffer=chunk)

print("* recording")
for i in range(0, 44100 // chunk * RECORD_SECONDS):
    data = stream.read(chunk)
    frames.append(data)
    # check for silence here by comparing the level with 0 (or some threshold) for 
    # the contents of data.
    # then write data or not to a file

print("* done")

stream.stop_stream()
stream.close()
p.terminate()

outputfile = os.path.join(gettempdir(), fileName)
myFile = wave.open(outputfile, 'wb')
myFile.setnchannels(CHANNELS)
myFile.setsampwidth(p.get_sample_size(FORMAT))
myFile.setframerate(RATE)
myFile.writeframes(b''.join(frames))
myFile.close()

if sys.platform == "win32":
    os.startfile(outputfile)
else:
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.Popen([opener, outputfile])