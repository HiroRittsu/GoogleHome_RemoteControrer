import matplotlib.pyplot as plt
import numpy as np


def main():
	data = np.loadtxt('../data/air_data_26', delimiter='\n', dtype='int')
	print(data)
	x = np.asanyarray([])
	y = np.asanyarray([])
	bits = ''
	t = 0
	for i in range(len(data)):
		if data[i] == 600:
			bits += '0'
		if data[i] == 1600:
			bits += '1'
		y = np.append(y, (-1) ** i)
		x = np.append(x, t)
		t += data[i]
		y = np.append(y, (-1) ** i)
		x = np.append(x, t)

	plt.plot(x, y)
	print(bits)
	hex = ''
	for i in range(0, len(bits), 8):
		print(bits[i:i + 8])
		hex += format(int(bits[i:i + 8], 2), 'x') + ' '
	# print(format(int(bit[i:i + 8], 2), 'x'))
	print(hex)
	plt.show()


if __name__ == '__main__':
	main()
