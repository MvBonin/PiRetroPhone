import os
import wave
import alsaaudio

from gtts import gTTS

language = 'de'

def textToSpeech(text, fileName):
    global language
    obj = gTTS(text=text, lang=language, slow=False)
    obj.save(fileName)
