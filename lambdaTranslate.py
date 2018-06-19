import boto3
import io
import json
import urllib


def getText():
    s3 = boto3.resource('s3')
    object = s3.Object('rainbowbird', 'transcripts/transcript.txt')
    transcript_uri = 'https://s3-us-west-2.amazonaws.com/rainbowbird/transcripts/transcript.json'
    f = urllib.request.urlopen(transcript_uri).read()
    data = json.load(f)
    print(data)
    
def translate():
    ts = boto3.resource('translate')
    
getText()