import csv


class KantaiCollectionVoice:
    def __init__(self, kc_ships_filepath: str, voice_key_filepath: str):
        self.kc_ships_filepath = kc_ships_filepath
        self.voice_key_filepath = voice_key_filepath

    def get_announcement_voice_url(self, ship_name: str, hour: int):
        with open(self.kc_ships_filepath) as fp:
            for line in csv.reader(fp):
                if line[1] == ship_name:
                    ship_info = (int(line[0]), line[2])
                    break
        with open(self.voice_key_filepath) as fp:
            voice_key = int(list(csv.reader(fp))[0][hour])

        voice_id = int(((ship_info[0] + 7) * 17 * voice_key) % 99173) + 100000

        result_url = f"http://203.104.209.71/kcs/sound/kc{ship_info[1]}/{voice_id}.mp3"

        return result_url


if __name__ == '__main__':
    print(
        KantaiCollectionVoice("../../data/kc_ships.csv", "../../data/voice_keys.csv").get_announcement_voice_url("ヴェールヌイ", 2)
    )

    print()
