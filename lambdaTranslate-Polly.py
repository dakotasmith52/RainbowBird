import boto3
import io
import json
import urllib
from urllib.request import Request, urlopen
from contextlib import closing
import sys
import os
from tempfile import gettempdir

s3 = boto3.resource('s3')
polly = boto3.client("polly")
ts = boto3.client(service_name='translate', region_name='us-west-2', use_ssl=True)

def getText():
    req = Request('https://s3-us-west-2.amazonaws.com/rainbowbird-translations/transcripts/transcript.txt', headers={'User-Agent':'Mozilla/5.0'})
    f = urllib.request.urlopen(req).read()
    decodedString = f.decode('utf-8')
    print(decodedString)
    return decodedString
    

def determineVoice(lang):
    pollyVoice = {'en': 'Amy', 'fr': 'Celine', 'de': 'Vicki', 'pt': 'Vitoria', 'es':'Enrique'}
    languageOptions = {'English': 'en', 'French': 'fr', 'German': 'de', 'Portugese': 'pt', 'Spanish':'es'}
    return pollyVoice[lang] if lang in pollyVoice else None
    
def translate():
    myobject = s3.Object('rainbowbird-translations', 'translations/translation.mp3')
    objACL = myobject.objACL
    targetLang = 'en'
    result = ts.translate_text(Text=getText(), 
            SourceLanguageCode='en', TargetLanguageCode=targetLang)
    targetlanguage = result.get('TargetLanguageCode')
    # Request speech synthesis
    response = polly.synthesize_speech(Text=result.get('TranslatedText'), OutputFormat="mp3",
                                        VoiceId=determineVoice(targetlanguage))
    if "AudioStream" in response:
    # Note: Closing the stream is important as the service throttles on the
    # number of parallel connections. Here we are using contextlib.closing to
    # ensure the close method of the stream object will be called automatically
    # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream2:
            output = os.path.join(gettempdir(), 'translation.mp3')

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
    myobject.put(Body=output)
    objACL.put(ACL='public-read')


def lambda_handler(event, context):
    translate()
    return 'Done!'
