import os
from langdetect import detect
from MeloTTS.melo.api import TTS
import simpleaudio as sa

class Speaker:
    def __init__(self, output_path: str):
        self.output_path = output_path
        self.languages = ['en','es', 'fr', 'jp', 'kr', 'zh']

    # Return the path of the output sound file
    def speak(self, text: str) -> str:
        lang = detect(text)
        if not lang in self.languages:
            return None
        
        model = TTS(language=lang.upper())

        speaker_ids = model.hps.data.spk2id
        speakers = list(speaker_ids.keys())
        speaker_id = speaker_ids[speakers[0]]

        wav_path = f'{self.output_path}/temp.wav'
        os.makedirs(os.path.dirname(wav_path), exist_ok=True)
        # Always choose the first speaker        
        model.tts_to_file(text, speaker_id, wav_path, speed=1.0)

        self.__play__(wav_path)

    def __play__(self, path):
        sound_file = f'{os.getcwd()}/{path}'
        wave_obj = sa.WaveObject.from_wave_file(sound_file)
        play_obj = wave_obj.play()
        play_obj.wait_done()  # Wait until sound has finished playing
        
        

