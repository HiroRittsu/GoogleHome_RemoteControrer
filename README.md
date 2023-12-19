curl "https://api.voicetext.jp/v1/tts" \
     -u "x2e8pmia42psrn10:" \
     -d "text=おはようございます" \
     -d "emotion=happiness" \
     -d "pitch=110" \
     -d "speed=150" \
     -d "volume=200" \
     -d "emotion_level=4" \
     -d "speaker=haruka" | play -

pip3 install blynk-library-python