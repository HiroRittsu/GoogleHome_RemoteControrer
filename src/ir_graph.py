import matplotlib.pyplot as plt
import numpy as np


def convert_bit(raw_list: list):
	table = {'350': '300', '650': '600', '1550': '1600', '550': '600'}
	bits = ''
	for i in range(len(raw_list)):
		if i == 0 or i == 1:
			continue

		if not i % 2 == 0:
			if int(raw_list[i]) > 1000:
				bits += '1'
			else:
				bits += '0'

		if (i - 1) % 16 == 0:
			bits += ' '

	return bits


def main():
	raw_data = input()
	raw_data_list = list(raw_data.replace(' ', '').split(','))
	bits = convert_bit(raw_data_list)

	print(bits)


if __name__ == '__main__':
	main()
