import copy


def xor_i(index: int, bit_l: str, bit_s: str):
	result = ''
	for i in range(len(bit_l)):
		if i >= index and i < index + len(bit_s):
			if bit_l[i] == bit_s[i - index]:
				result += '0'
			else:
				result += '1'
		else:
			result += bit_l[i]

	return result


def main():
	result = []
	raw_bit = input()
	original_error_bit = raw_bit.replace(' ', '')[-4:]
	raw_bit = raw_bit.replace(' ', '')[:-4]
	for i in range(16, 32):
		divisor = format(i, 'b').zfill(5)
		target = copy.deepcopy(raw_bit)
		# print(divisor)
		for j in range(len(target) - 4):
			if target[j] == '0':
				continue
			target = xor_i(j, target, divisor)
		# print(target)
		if original_error_bit == target[-4:]:
			result.append(divisor)
	print(result)


if __name__ == '__main__':
	main()
