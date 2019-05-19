import os
import shutil

import datetime
import subprocess
import configparser
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import requests

app = Flask(__name__)

ini_file = configparser.ConfigParser()
ini_file.read('./token.ini')

API_KEY = ini_file.get('token', 'API_KEY')
url = "https://api.apigw.smt.docomo.ne.jp/aiTalk/v1/textToSpeech?APIKEY=" + API_KEY

HOST = "192.168.11.9"
# HOST = "127.0.0.1"

ship_data = {}
voice_keys = []


def picked_up():
	messages = [
		"こんにちは！",
		"やあ！",
		"へい！"
	]
	# NumPy の random.choice で配列からランダムに取り出し
	return np.random.choice(messages)


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


def docomo_api_voice(prm):
	media_dir = './media/'
	shutil.rmtree(media_dir)
	os.mkdir(media_dir)
	# SSML生成
	# ===========================================
	xml = u'<?xml version="1.0" encoding="utf-8" ?>'
	voice = '<voice name="' + prm["speaker"] + '">'
	prosody = '<prosody rate="' + str(prm['rate']) + '" pitch="' + str(prm['pitch']) + '" range="' + str(prm['range']) + '">'
	xml += '<speak version="1.1">' + voice + prosody + str(prm['text']) + '</prosody></voice></speak>'
	# utf-8にエンコード
	xml = xml.encode("UTF-8")

	print(xml)
	print(len(xml))
	
	response = requests.post(
		url,
		data=xml,
		headers={
			'Content-Type': 'application/ssml+xml',
			'Accept': 'audio/L16',
			'Content-Length': str(len(xml))
		}
	)

	if response.status_code != 200:
		print("Error API : " + response.status_code)
		exit()
	else:
		print("Success API")

	now = datetime.datetime.now()
	tstr = datetime.datetime.strftime(now, '%Y%m%d-%H%M%S')

	# バイナリデータを保存
	raw_name = tstr + '.raw'
	fp = open(media_dir + raw_name, 'wb')
	fp.write(response.content)
	fp.close()

	wav_name = tstr + '.mp3'
	# soxを使って raw→wavに変換
	cmd = "sox -t raw -r 16k -e signed -b 16 -B -c 1 " + media_dir + raw_name + " " + media_dir + wav_name + " gain -l 10"
	# コマンドの実行
	subprocess.check_output(cmd, shell=True)

	return wav_name


def get_voice(args):
	if not len(args) == 6:
		return

	speaker = args.get('speaker').replace('\'', '')
	pitch = args.get('pitch').replace('\'', '')
	range = args.get('range').replace('\'', '')
	rate = args.get('rate').replace('\'', '')
	volume = args.get('volume').replace('\'', '')
	text = args.get('text').replace('\'', '')

	prm = {
		'speaker': speaker,
		'pitch': pitch,
		'range': range,
		'rate': rate,
		'volume': volume,
		'text': text
	}

	print(text)

	media_name = docomo_api_voice(prm)
	url = "http://" + HOST + ":8000/media/" + media_name
	return url


def get_kc_time_voice_url(ship_name: str, voice_key: int):
	print(ship_name)
	ship = ship_data[ship_name]
	voice_id = calc_kc_voice_id(int(ship[0]), voice_key)
	return "http://203.104.209.71/kcs/sound/kc" + ship[1] + "/" + str(voice_id) + ".mp3"


def calc_kc_voice_id(ship_id: int, voice_key: int):
	return int(((ship_id + 7) * 17 * voice_key) % 99173) + 100000


@app.route('/')
def index():
	title = "ようこそ"
	message = picked_up()
	# index.html をレンダリングする
	return render_template('index.html', message=message, title=title)


@app.route('/help')
def help():
	return " speaker   :  nozomi 、 seiji 、 akari 、 anzu 、 hiroshi 、 kaho 、 koutarou 、 maki 、 nanako 、 osamu 、 sumire <br>" \
		   "   pitch   : ベースライン・ピッチ。 基準値:1.0、範囲:0.50～2.00<br>" \
		   "   range   : ピッチ・レンジ。基準値:1.0、範囲:0.00～2.00<br>" \
		   "    rate   : 読み上げる速度。基準値:1.0、範囲:0.50～4.00<br>" \
		   "  volume   : 音量。基準値:1.0、範囲:0.00～2.00<br>" \
		   "    text   : 読み上げるテキスト<br>" \
		   " (example) : http://" + HOST + ":8000/textToSpeech?speaker='sumire'&pitch=1&range='1.04'&rate='1.3'&volume='2'&text='朝だよ―'"


@app.route('/textToSpeech')
def response():
	return get_voice(request.args)


@app.route('/media/<path:path>')
def media(path):
	return send_from_directory("./media/", path)


@app.route('/timeReport/<path:path>')
def time_report(path):
	file_name = np.random.choice(['./data/time_report_list_yukari.csv', './data/time_report_list_maki.csv'])
	time_report = np.loadtxt(file_name, delimiter='\n', dtype='str')
	return time_report[int(path)]


@app.route('/timeReportKC')
def timeReportKC():
	ships = ["ヴェールヌイ", "金剛改二", "比叡改二", "夕張", "夕立改二"]
	url = get_kc_time_voice_url(np.random.choice(ships), voice_keys[int(request.args.get('time'))])
	return url


if __name__ == '__main__':
	read_ship()
	app.run(debug=False, host=HOST, port=8000)
