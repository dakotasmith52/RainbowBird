from __future__ import print_function
import boto3
from boto3 import Session
import time
from random import randint

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
        print("Not ready yet...")
    time.sleep(5)

print(status)
print(job_name)