import os
import time
from datetime import datetime

import BlynkLib
import numpy as np
import schedule

from modules.google_home_notifier import GoogleHomeNotifier
from modules.voice_vox_api import VoiceVoxAPI
from src.modules.kantai_collection_voice import KantaiCollectionVoice

SHIPS = ["ヴェールヌイ", "夕張", "夕立改二", "吹雪改", "金剛改", "比叡改", "榛名改", "霧島改", "暁改", "長門改", "鈴谷",
         "大和", "武蔵", "加賀改"]


class GoogleHomeServer:
    def __init__(self):
        self.google_home_device = GoogleHomeNotifier(friendly_names=["ダイニング ルーム"])
        self.voice_api = VoiceVoxAPI(speaker_name="VOICEVOX:ずんだもん（ノーマル）",
                                     speakers_filepath="../data/voicevox_speakers.json")
        self.kc_voice = KantaiCollectionVoice("../data/kc_ships.csv", "../data/voice_keys.csv")

    def task_announcement(self):
        print("時報")
        voice_url = self.kc_voice.get_announcement_voice_url(np.random.choice(SHIPS),
                                                             int(datetime.now().strftime("%H")))
        self.google_home_device.play(voice_url)

    def speak_text(self, text):
        voice_url = self.voice_api.get_voice_url(text)
        self.google_home_device.play(voice_url)


def main():
    blynk = BlynkLib.Blynk(os.environ.get("BLYNK_TOKEN"), **{"server": "blynk.cloud"})
    gh_server = GoogleHomeServer()

    # スケジュール登録
    # schedule.every().hour.at(":15").do(gh_server.task_announcement)
    schedule.every(5).minutes.do(gh_server.task_announcement)

    @blynk.VIRTUAL_WRITE(1)
    def virtual_1(value):
        print("v1", value)

    gh_server.speak_text("開始します。")

    while True:
        schedule.run_pending()
        blynk.run()
        time.sleep(1)


if __name__ == '__main__':
    main()
