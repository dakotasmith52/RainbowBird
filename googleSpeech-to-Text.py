def transcribe():
    os.system("gcloud ml speech recognize "+ outputfile +" --language-code='en-US' > transcription.json")
    with open('transcription.json', 'r') as f:
        tsfile = json.load(f)
    transcription = tsfile['results'][0]['alternatives'][0]['transcript']
    return transcription