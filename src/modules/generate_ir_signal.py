"""
http://elm-chan.org/docs/ir_format.html
"""
import numpy as np


class GenerateIrSignal:
    def __init__(self):
        pass

    @staticmethod
    def rle(sequence: np.ndarray):
        comp_seq_index, = np.concatenate(([True], sequence[1:] != sequence[:-1], [True])).nonzero()
        return sequence[comp_seq_index[:-1]], np.ediff1d(comp_seq_index)

    @staticmethod
    def covert_str_bit(bit_data: str):
        return [int(x) for x in bit_data]

    def sharp_air_conditioner(self, temperature: int, mode: str) -> list:
        result_data = []
        if temperature == -1:
            result_data.extend([9000, 4500])
            result_data.extend(self.covert_str_bit("00110000000100000000011000000011111"))
            result_data.extend([650, 20000])
            result_data.extend(self.covert_str_bit("00000000000000010000000000001101"))

        else:
            pass

        result_data.extend([650, 40000])
        result_data.extend([9000, 4500])
        result_data.extend(self.covert_str_bit("00000000000000000000000000000111111"))
        result_data.extend([650, 20000])
        result_data.extend(self.covert_str_bit("00000000000000000000000000001111"))
        result_data.append(650)  # 終了ビット

        return result_data


if __name__ == '__main__':
    print(GenerateIrSignal().sharp_air_conditioner(-1, ""))
    # print(len(GenerateIrSignal().sharp_air_conditioner(-1, "")))
    encoded_raw_data = GenerateIrSignal().rle(np.asarray(GenerateIrSignal().sharp_air_conditioner(-1, "")))
    print(
        "{\"raw_data\":" + f"{list(encoded_raw_data[0])}" + ", \"length\": " + f"{list(encoded_raw_data[1])}" + "}")
