import os
import shutil

import datetime
import configparser
from flask import Flask, request, send_from_directory
import numpy as np
import requests

app = Flask(__name__)

ini_file = configparser.ConfigParser()
ini_file.read('./token.ini')

API_KEY = ini_file.get('token', 'API_KEY')

HOST = "192.168.11.9"
# HOST = "127.0.0.1"

ship_data = {}
voice_keys = []


def read_csv(path):
    with open(path) as f:
        for line in f.readlines():
            data = line.replace('\n', '').split(',')
            ship_data.setdefault(data[1], [data[0], data[2]])


def read_ship():
    with open('./data/kc_ships.csv') as f:
        for line in f.readlines():
            data = line.replace('\n', '').split(',')
            ship_data.setdefault(data[1], [data[0], data[2]])

    with open('./data/voice_key.csv') as f:
        for key in f.read().split(','):
            voice_keys.append(int(key))


def voice_text_api(text):
    media_dir = './media/'
    shutil.rmtree(media_dir)
    os.mkdir(media_dir)

    payload = {
        'text': text,
        'speaker': 'haruka',
        'emotion': 'happiness',
        'emotion_level': '1',
        'pitch': '130',
        'speed': '110',
        'volume': '200'
    }

    url = "https://" + API_KEY + ":@api.voicetext.jp/v1/tts"

    post_response = requests.post(url, params=payload, auth=(API_KEY, ''))

    if post_response.status_code != 200:
        print("Error API : " + post_response.status_code)
        exit()
    else:
        print("Success API")

    now = datetime.datetime.now()
    tstr = datetime.datetime.strftime(now, '%Y%m%d-%H%M%S')

    # バイナリデータを保存
    wav_name = tstr + '.wav'
    fp = open(media_dir + wav_name, 'wb')
    fp.write(post_response.content)
    fp.close()

    return wav_name


def get_kc_time_voice_url(ship_name: str, voice_key: int):
    print(ship_name)
    ship = ship_data[ship_name]
    voice_id = calc_kc_voice_id(int(ship[0]), voice_key)
    return "http://203.104.209.71/kcs/sound/kc" + ship[1] + "/" + str(voice_id) + ".mp3"


def calc_kc_voice_id(ship_id: int, voice_key: int):
    return int(((ship_id + 7) * 17 * voice_key) % 99173) + 100000


@app.route('/text_to_voice')
def response():
    """
    テキストから音声ファイルに変換
    :return:
    """
    if not len(request.args) == 1:
        return
    text = request.args.get('text').replace('\'', '')
    print(text)
    media_name = voice_text_api(text)
    request_url = "http://" + HOST + ":8000/media/" + media_name
    return request_url


@app.route('/media/<path:path>')
def media(path):
    return send_from_directory("./media/", path)


@app.route('/timeReportKC')
def time_report_kc():
    ships = ["ヴェールヌイ", "金剛改二", "比叡改二", "夕張", "夕立改二"]
    request_url = get_kc_time_voice_url(np.random.choice(ships), voice_keys[int(request.args.get('time'))])
    return request_url


@app.route('/checkStatus')
def check_status():
    return "ok"


if __name__ == '__main__':
    read_ship()
    app.run(debug=False, host=HOST, port=8000)
