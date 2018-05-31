from __future__ import print_function
import boto3
from boto3 import Session
import time
from random import randint
import urllib
import os
from tempfile import gettempdir
import subprocess
import contextlib
import json

session = Session(profile_name='default')
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