"""
https://github.com/ts-klassen/ttsQuestV3Voicevox
"""
import json
import time

import requests


class VoiceVoxAPI:
    def __init__(self, speaker_name: str, speakers_filepath: str):
        with open(speakers_filepath, mode='r') as fp:
            self.speaker_id = list(json.load(fp)).index(speaker_name)

    def get_voice_url(self, text):
        print(text)
        url = f"https://api.tts.quest/v3/voicevox/synthesis?speaker={self.speaker_id}&text={text}"
        request = requests.get(url)
        if request.status_code != 200:
            print("Error API : " + str(request.status_code))
            exit()
        else:
            print("Success API")
        result_url = request.json()["mp3DownloadUrl"]

        while True:
            # 音声ファイル生成状況確認
            status = requests.get(str(result_url).replace("audio.mp3", "status.json"))
            if status.json()["isAudioReady"]:
                break
            time.sleep(0.5)
            print("生成待ち")

        return result_url


if __name__ == '__main__':
    VoiceVoxAPI(
        speaker_name="VOICEVOX:ずんだもん（ヒソヒソ）",
        speakers_filepath="../../data/voicevox_speakers.json"
    ).get_voice_url("おはようございます")
