def convert_bit(raw_list: list):
	bits = ''
	for i in range(len(raw_list)):
		if i == 0 or i == 1:
			continue

		if not i % 2 == 0:
			if int(raw_list[i]) > 1000:
				bits += '1'
			else:
				bits += '0'

	# if (i - 1) % 16 == 0:
	# bits += ' '

	return bits


def convert_hex(bits: str):
	hexs = ''
	bits = bits.replace(' ', '')
	for i in range(0, len(bits) - 3, 4):
		hexs += hex(int(bits[i:i + 4][::-1], 2)).replace('0x', '')

	return hexs


def main():
	raw_data = input()
	raw_data_list = list(raw_data.replace(' ', '').split(','))
	bits = convert_bit(raw_data_list)

	print(convert_hex(bits))


if __name__ == '__main__':
	main()
