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

# Set stream variables and quality
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

fileName = "recording.wav"
# Create a file in the temporary directory
outputfile = os.path.join(gettempdir(), fileName)
p = pyaudio.PyAudio()
frames = []

# Create stream
stream = p.open(format=FORMAT,
                channels=CHANNELS, 
                rate=RATE, 
                input=True,
                output=True,
                frames_per_buffer=chunk)

def recordme(x):
    record()
    end_stream()
    writefile()
    upload(x)

def record():
    print("* recording")
    # Start writing data to the empty frames array, each frame. Frames are derived by the following equation.
    for i in range(0, 44100 // chunk * RECORD_SECONDS):
        data = stream.read(chunk)
        frames.append(data)
        # check for silence here by comparing the level with 0 (or some threshold) for 
        # the contents of data.
        # then write data or not to a file

    print("* done")

def end_stream():
    # Stop the stream and terminate the process
    stream.stop_stream()
    stream.close()
    p.terminate()


def writefile():
    # Save the output of that stream to the file you just created in wav format.
    myFile = wave.open(outputfile, 'wb')
    myFile.setnchannels(CHANNELS)
    myFile.setsampwidth(p.get_sample_size(FORMAT))
    myFile.setframerate(RATE)
    myFile.writeframes(b''.join(frames))
    myFile.close()

def upload(x):
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(x,'jedijamez-projects','RainbowBird/recording.wav')


recordme(outputfile)