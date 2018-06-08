import os
import io
from tempfile import gettempdir
import subprocess
import json

filename = 'transcript.json'
def transcribe():
    os.system("gcloud ml speech recognize recording.wav --language-code='en-US' > transcription.json")
    with open('transcription.json', 'r') as f:
        tsfile = json.load(f)

    print(tsfile['results'][0]['alternatives'][0]['transcript'])

transcribe()