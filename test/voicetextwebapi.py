import datetime
import requests

API_KEY = 'mrltjhlqwe5mki19'
url = "https://" + API_KEY + ":@api.voicetext.jp/v1/tts"
text = input(">>")

payload = {
    'text': text,
    'speaker': 'haruka',
    'emotion': 'happiness',
    'emotion_level': '1',
    'pitch': '130',
    'speed': '110'
}

response = requests.post(url, params=payload, auth=(API_KEY, ''))

if response.status_code != 200:
    print("Error API : " + response.status_code)
    exit()

else:
    print("Success API")

# 現在日時を取得
now = datetime.datetime.now()
tstr = datetime.datetime.strftime(now, '%Y%m%d-%H%M%S')

# 保存するファイル名
rawFile = tstr + ".wav"

# バイナリデータを保存
fp = open(rawFile, 'wb')
fp.write(response.content)
fp.close()
