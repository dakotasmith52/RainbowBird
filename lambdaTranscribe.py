import boto3
from random import randint
import time
import urllib
import json
from tempfile import gettempdir
import io
import json

def transcribe():
    s3 = boto3.resource('s3')
    obj = s3.Object('rainbowbird', 'transcripts/transcript.json')
    ts = boto3.client('transcribe')
    job_name = str(randint(0,999))
    job_uri = 'https://s3-us-west-2.amazonaws.com/rainbowbird/recording/Recording.wav'
    print('starting transcription job...')
    ts.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri':job_uri},
        MediaFormat='wav',
        LanguageCode='en-US'
    )
    print('started transcription job ' + job_name + '.')
    while True:
        status = ts.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            print ('Status: ' + status['TranscriptionJob']['TranscriptionJobStatus'])
            break
        print('not done yet...')
        time.sleep(1)
        
    transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    f = urllib.request.urlopen(transcript_uri).read()
    memfile = io.BytesIO(f)
    datastore = json.load(memfile)
    transcription = datastore['results']['transcripts'][0]['transcript']
    # PUT request for S3 to create transcript file in s3://rainbowbird/transcripts/transcript.txt
    print('creating s3 object...')
    obj.put(Body=transcription)

transcribe()