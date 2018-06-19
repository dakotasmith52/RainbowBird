from pydub import AudioSegment
from tempfile import gettempdir
import os

def convert(x):
	mypath = os.path.join(gettempdir(), 'wavfile.wav')
	sound = AudioSegment.from_mp3(x)
	convertedwav = sound.export(mypath, format='wav')
	return convertedwav
