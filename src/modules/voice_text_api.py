import os
from pathlib import Path
import requests


class VoiceTextAPI:
    def __init__(self, media_dir="", wav_filename="voice.wav"):
        self.payload = {
            "text": "",
            "speaker": "haruka",
            "emotion": "happiness",
            "emotion_level": "4",
            "pitch": "100",
            "speed": "120",
            "volume": "200"
        }
        self.wav_filename = Path(media_dir).joinpath(wav_filename)
        self.api_key = os.environ.get("VOICE_TEXT_API_KEY")

    def get_voice(self, text):
        self.payload["text"] = text
        url = f"https://{self.api_key}:@api.voicetext.jp/v1/tts"
        post_response = requests.post(url, params=self.payload, auth=(self.api_key, ''))

        if post_response.status_code != 200:
            print("Error API : " + str(post_response.status_code))
            exit()
        else:
            print("Success API")

        # バイナリデータを保存
        with open(self.wav_filename, 'wb') as fp:
            fp.write(post_response.content)
        return self.wav_filename


if __name__ == '__main__':
    VoiceTextAPI(media_dir="../../media").get_voice("おはようございます")
