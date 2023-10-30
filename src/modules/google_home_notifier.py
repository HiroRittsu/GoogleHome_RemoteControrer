import pychromecast


class GoogleHomeNotifier:
    def __init__(self, friendly_names: list):
        devices, _ = pychromecast.get_listed_chromecasts(friendly_names=friendly_names)
        if len(devices) == 0:
            print("Google Homeが見つかりません")
            exit()
        self.device = devices[0]

    def play(self, media_file_url):
        if not self.device.is_idle:
            print("Killing current running app")
            self.device.quit_app()

        # 喋らせる
        print(media_file_url)
        mc = self.device.media_controller
        self.device.wait()
        mc.play_media(media_file_url, 'audio/mp3')
        mc.block_until_active()


if __name__ == '__main__':
    google_home = GoogleHomeNotifier(friendly_names=["ダイニング ルーム"])
    google_home.play("http://192.168.10.106/20190519-144616.mp3")
