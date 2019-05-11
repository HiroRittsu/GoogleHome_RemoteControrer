#include <stdio.h>
#include <stdlib.h>

/*
16進数のコードから
２進数変換
誤り検知符号
raw_data変換
*/

int size(char* array) {
	int count = 0;
	while (*array++ != '\0') count++;
	return count;
}

char* int2bin(int x) {
	static char bin[4];
	for (int i = 0; i < 4; ++i) bin[i] = ((x >> i) & 1 ) + '0';
	return bin;
}

void convert(char* hexs, char* bits) {
	char table[] = "0123456789abcdef";
	int* ints = (int *)malloc(size(hexs) * sizeof(int));
	//16進数から10進数に変換
	for (int i = 0; i < size(hexs); ++i) {
		for (int t = 0; t < 16; ++t) {
			if (hexs[i] == table[t]) {
				ints[i] = t;
				break;
			}
		}
	}
	//10進数から2進数に変換
	for (int i = 0; i < size(hexs); ++i) {
		char* tmp = int2bin(ints[i]);
		for (int c = 0; c < 4; ++c) {
			*bits++ = tmp[c];
		}
	}
}

void calc_error_detection(char* bits, char* error, char* divisor) {
	char* result_bits = (char *)malloc(size(bits) * sizeof(char));
	for (int i = 0; i < size(bits); ++i) result_bits[i] = bits[i];
	for (int divisor_target = 0; divisor_target < size(bits) - 4; ++divisor_target) {
		if (result_bits[divisor_target] == '0') continue;
		for (int i = 0; i < size(bits); ++i) {
			if (i >= divisor_target && i < divisor_target + 5) {
				if (result_bits[i] == divisor[i - divisor_target])
					result_bits[i] = '0';
				else
					result_bits[i] = '1';
			}
		}
	}
	for (int i = 0; i < 4; ++i) error[i] = result_bits[size(bits) - 4 + i];
}


void add_error_detection(char* bits, char* divisor) {
	char error_detection[4];
	calc_error_detection(bits, error_detection, divisor);
	for (int i = 0; i < 5; ++i) {
		bits[size(bits)] = error_detection[i];
		bits[size(bits) + 1] = '\0';
	}
}

unsigned int* generate_ir_data(char* bits, int* times) {
	unsigned int* rawData = (unsigned int*)malloc(((size(bits) + 2) * 2 - 1) * sizeof(unsigned int));
	*rawData++ = times[0];
	*rawData++ = times[1];
	for (int i = 0; i < size(bits); ++i) {
		*rawData++ = times[2];
		if (bits[i] == '0')
			*rawData++ = times[3];
		else
			*rawData++ = times[4];
	}
	*rawData++ = times[2];
	*rawData = 0;
	rawData -= ((size(bits) + 2) * 2 - 1);
	return rawData;
}

unsigned int* aircon_data(char* hexs) {
	char* bits = (char *)malloc((size(hexs) * 4 + 4) * sizeof(char));
	int times[] = {3750, 2050, 300, 600, 1600};
	unsigned int* rawData;
	convert(hexs, bits);
	add_error_detection(bits, "10001");
	rawData = generate_ir_data(bits, times);
	printf("%s\n", bits );
	return rawData;
}

unsigned int* light_data(char* hexs) {
	char* bits = (char *)malloc((size(hexs) * 4 + 4) * sizeof(char));
	int times[] = {3500, 1750, 400, 400, 1300};
	unsigned int* rawData;
	convert(hexs, bits);
	rawData = generate_ir_data(bits, times);
	printf("%s\n", bits );
	return rawData;
}

int main(int argc, char const *argv[]) {
	unsigned int*  rawData;
	rawData = aircon_data("aaa5fc0180122200800a004e1");
	//rawData = light_data("c22590d242");
	while (*rawData != 0) printf("%d,", *rawData++);
	return 0;
}