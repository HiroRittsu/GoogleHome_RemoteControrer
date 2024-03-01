import os
import time
from datetime import datetime

import BlynkLib
import numpy as np
import requests
import schedule

from modules.generate_ir_signal import GenerateIRSignal
from modules.google_home_notifier import GoogleHomeNotifier
from modules.kantai_collection_voice import KantaiCollectionVoice
from modules.voice_vox_api import VoiceVoxAPI

ARDUINO_URL = "http://192.168.10.106/"
SHIPS = [
    "ヴェールヌイ",
    "夕張",
    "夕立改二",
    "吹雪改",
    "金剛改",
    "比叡改",
    "榛名改",
    "霧島改",
    "暁改",
    "長門改",
    "鈴谷",
    "大和",
    "武蔵",
    "加賀改",
]


class GoogleHomeServer:
    def __init__(self):
        self.google_home_device = GoogleHomeNotifier(
            friendly_names=["ダイニング ルーム"]
        )
        self.voice_api = VoiceVoxAPI(
            speaker_name="VOICEVOX:ずんだもん（ノーマル）",
            speakers_filepath="../data/voicevox_speakers.json",
        )
        self.kc_voice = KantaiCollectionVoice(
            "../data/kc_ships.csv", "../data/voice_keys.csv"
        )
        self.do_announcement = False

    def task_announcement(self):
        """
        時報実行
        :return:
        """
        if self.do_announcement:
            print("時報")
            voice_url = self.kc_voice.get_announcement_voice_url(
                np.random.choice(SHIPS), int(datetime.now().strftime("%H"))
            )
            self.google_home_device.play(voice_url)

    def speak_text(self, text):
        voice_url = self.voice_api.get_voice_url(text)
        self.google_home_device.play(voice_url)


def main():
    blynk = BlynkLib.Blynk(os.environ.get("BLYNK_TOKEN"), **{"server": "blynk.cloud"})
    gh_server = GoogleHomeServer()
    generate = GenerateIRSignal()

    @blynk.VIRTUAL_WRITE(1)
    def virtual_1(value):
        """
        照明 ON/OFF
        :param value:
        :return:
        """
        pass

    @blynk.VIRTUAL_WRITE(2)
    def virtual_2(value):
        """
        空調自動制御
        :param value:
        :return:
        """
        response = requests.get(
            f"{ARDUINO_URL}/raw_data?json={generate.koizumi_ceiling_light_alternate()}"
        )

    @blynk.VIRTUAL_WRITE(3)
    def virtual_3(value):
        """
        暖房 OFF/温度指定
        :param value:
        :return:
        """
        print("v3", value)
        if 16 < value[0] < 30:
            response = requests.get(
                f"{ARDUINO_URL}/raw_data?json={generate.sharp_air_conditioner(0, value[0])}"
            )
        else:
            # 停止
            response = requests.get(
                f"{ARDUINO_URL}/raw_data?json={generate.sharp_air_conditioner(-1, -1)}"
            )

    @blynk.VIRTUAL_WRITE(4)
    def virtual_4(value):
        """
        冷房 OFF/温度指定
        :param value:
        :return:
        """
        print("v4", value)
        if 16 < value[0] < 30:
            response = requests.get(
                f"{ARDUINO_URL}/raw_data?json={generate.sharp_air_conditioner(2, value[0])}"
            )
        else:
            # 停止
            response = requests.get(
                f"{ARDUINO_URL}/raw_data?json={generate.sharp_air_conditioner(-1, -1)}"
            )

    @blynk.VIRTUAL_WRITE(5)
    def virtual_5(value):
        """
        時報 ON/OFF
        :param value:
        :return:
        """
        print("v5", value)
        if value[0] == "1":
            print("時報ON")
            gh_server.do_announcement = True
        else:
            print("時報OFF")
            gh_server.do_announcement = False

    # スケジュール登録
    schedule.every().hour.at(":00").do(gh_server.task_announcement)
    gh_server.speak_text("開始します。")

    while True:
        schedule.run_pending()
        blynk.run()
        time.sleep(1)


if __name__ == "__main__":
    main()
