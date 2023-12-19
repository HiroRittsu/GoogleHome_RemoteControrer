"""
http://elm-chan.org/docs/ir_format.html
"""
import json
import numpy as np
import requests


class GenerateIRSignal:
    def __init__(self):
        pass

    @staticmethod
    def encode_rle(sequence: np.ndarray):
        comp_seq_index, = np.concatenate(([True], sequence[1:] != sequence[:-1], [True])).nonzero()
        return sequence[comp_seq_index[:-1]], np.ediff1d(comp_seq_index)

    @staticmethod
    def covert_str_bit(bit_data: str):
        return [int(x) for x in bit_data]

    def koizumi_ceiling_light_alternate(self):
        result_data = []
        result_data.extend([9000, 4500])
        result_data.extend(self.covert_str_bit("00000001011101101111000000001111"))
        result_data.append(650)  # 終了ビット

        encoded_data = self.encode_rle(np.asarray(result_data))
        json_object = {
            "khz": 38,
            "base_time": 650,
            "negative_time": 550,
            "positive_time": 1600,
            "comp_array": list(encoded_data[0].astype(str)),
            "length_array": list(encoded_data[1].astype(str)),
        }

        return json.dumps(json_object)

    def sharp_air_conditioner(self, mode: int, temperature: int):
        """
        :param temperature:
        :param mode: 0=暖房, 1=除湿, 2=冷房
        :return: 圧縮済み信号データ
        """
        mode_list = ["00110000", "01011000", "10010000"]
        result_data = []
        result_data.extend([9000, 4500])
        if mode == -1:
            result_data.extend(self.covert_str_bit("00100000000100000000010000000011111"))
            result_data.extend([650, 20000])
            result_data.extend(self.covert_str_bit("00000000000000010000000000001100"))
        else:
            bin_v1 = format(temperature - 16, '04b')[3::-1]
            print(bin_v1, f"{mode_list[mode]}{bin_v1}00000000011000000011111")
            result_data.extend(self.covert_str_bit(f"{mode_list[mode]}{bin_v1}00000000011000000011111"))
            result_data.extend([650, 20000])

            if mode == 0:
                bin_v2 = format(temperature - 13, '04b')[3::-1]
                result_data.extend(self.covert_str_bit(f"0000000000000001000000000000{bin_v2}"))
                print(bin_v2, f"0000000000000001000000000000{bin_v2}")
            elif mode == 2:
                bin_v2 = format(temperature - 16, '04b')[3::-1]
                result_data.extend(self.covert_str_bit(f"1000000000000001000000000000{bin_v2}"))
                print(bin_v2, f"1000000000000001000000000000{bin_v2}")
            else:
                bin_v2 = format(temperature - 15, '04b')[3::-1]
                result_data.extend(self.covert_str_bit(f"0000000000000001000000000000{bin_v2}"))
                print(bin_v2, f"0000000000000001000000000000{bin_v2}")

        result_data.extend([650, 40000])
        result_data.extend([9000, 4500])
        result_data.extend(self.covert_str_bit("00000000000000000000000000000111111"))
        result_data.extend([650, 20000])
        result_data.extend(self.covert_str_bit("00000000000000000000000000001111"))
        result_data.append(650)  # 終了ビット

        encoded_data = self.encode_rle(np.asarray(result_data))
        json_object = {
            "khz": 38,
            "base_time": 650,
            "negative_time": 550,
            "positive_time": 1600,
            "comp_array": list(encoded_data[0].astype(str)),
            "length_array": list(encoded_data[1].astype(str)),
        }

        return json.dumps(json_object)


if __name__ == '__main__':
    response = requests.get(
        f"http://192.168.10.106/raw_data?json={GenerateIRSignal().koizumi_ceiling_light_alternate()}")
    # response = requests.get(f"http://192.168.10.106/raw_data?json={GenerateIRSignal().sharp_air_conditioner(0, 24)}")
    print(response.content)
