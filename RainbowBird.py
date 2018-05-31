from __future__ import print_function
import pyaudio
import time
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
import contextlib
import json
from random import randint
import urllib

# Recordme Script
# =========================================================================
# Records audio

# Set stream variables and quality
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = int(input('seconds to record: '))

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
                output=False,
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

# End of Recordme Script
# =========================================================================
# Start of Transcribe Script
# =========================================================================
# Converts .wav stored in S3 to text


session = Session(profile_name='default', region_name='us-west-2')
ts = boto3.client('transcribe')
job_name = str(randint(0,999))
job_uri = 'https://s3-us-west-2.amazonaws.com/jedijamez-projects/RainbowBird/recording.wav'
ts.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri':job_uri},
    MediaFormat='wav',
    LanguageCode='en-US'
)
while True:
    status = ts.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    time.sleep(1)

transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']

dlfile = os.path.join(gettempdir(), 'ts.json')
f = urllib.request.urlopen(transcript_uri)
with open(dlfile, 'wb') as code:
    code.write(f.read())

with open(dlfile) as x:
    datastore = json.load(x)

subprocess.Popen(['open', dlfile])
transcription = datastore['results']['transcripts'][0]['transcript']
print(transcription)
    

# End of Transcribe script
# =========================================================================
# Start of Translate and Polly Script
# =========================================================================
# Translates text returned from Transcribe into set language and writes audio file with Polly on local machine.

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
polly = session.client("polly")
pollyVoice = {'en': 'Amy', 'fr': 'Celine', 'de': 'Vicki', 'pt': 'Vitoria'}
languageOptions = {'English': 'en', 'French': 'fr', 'German': 'de', 'Portugese': 'pt'}
text = transcription

def mytargetlang():
    while True:
        for key in languageOptions:
            print (key,":",languageOptions[key])
        tlcode = input('please enter the language code: ')
        for key in languageOptions:
            if tlcode != languageOptions[key]:
                continue
            else:
                return tlcode

def readfile(f):
    readfile = open(f, 'r')
    txt = readfile.read(1000)
    return txt

translate = boto3.client(service_name='translate', region_name='us-west-2', use_ssl=True)
result = translate.translate_text(Text=text, 
            SourceLanguageCode='auto', TargetLanguageCode=(mytargetlang()))
# print('TranslatedText: ' + result.get('TranslatedText'))
# print('SourceLanguageCode: ' + result.get('SourceLanguageCode'))
# print('TargetLanguageCode: ' + result.get('TargetLanguageCode'))
targetlanguage = result.get('TargetLanguageCode')

def determineVoice(lang):
    return pollyVoice[lang] if lang in pollyVoice else None

try:
    # Request speech synthesis
    response = polly.synthesize_speech(Text=result.get('TranslatedText'), OutputFormat="mp3",
                                        VoiceId=determineVoice(targetlanguage))
except (BotoCoreError, ClientError) as error:
    # The service returned an error, exit gracefully
    print(error)
    sys.exit(-1)

# Access the audio stream from the response
if "AudioStream" in response:
    # Note: Closing the stream is important as the service throttles on the
    # number of parallel connections. Here we are using contextlib.closing to
    # ensure the close method of the stream object will be called automatically
    # at the end of the with statement's scope.
    with closing(response["AudioStream"]) as stream2:
        output = os.path.join(gettempdir(), "speech.mp3")

        try:
            # Open a file for writing the output as a binary stream
            with open(output, "wb") as file:
                file.write(stream2.read())
        except IOError as error:
            # Could not write to file, exit gracefully
            print(error)
            sys.exit(-1)
else:
    # The response didn't contain audio data, exit gracefully
    print("Could not stream audio")
    sys.exit(-1)

# Play the audio using the platform's default player
if sys.platform == "win32":
    os.startfile(output)
else:
    # the following works on Mac and Linux. (Darwin = mac, xdg-open = linux).
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.Popen([opener, output])
