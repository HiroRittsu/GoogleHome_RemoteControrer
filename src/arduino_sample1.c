#include <stdio.h>
#include <string.h>

#define HEX_NUMBER 25
#define BIT_NUMBER 100
#define DIVISOR "10001"

/*

16進数のコードから
２進数変換
誤り検知符号
raw_data変換

*/


char* int2bin(int x) {
	static char bin[4];
	for (int i = 0; i < 4; ++i) {
		bin[i] = ((x >> i) & 1 ) + '0';
	}
	return bin;
}

void convert(char* hexs, char* bits) {
	char table[] = "0123456789abcdef";
	int ints[HEX_NUMBER];

	//16進数から10進数に変換
	for (int i = 0; i < HEX_NUMBER; ++i) {
		for (int t = 0; t < 16; ++t) {
			if (hexs[i] == table[t]) {
				ints[i] = t;
				break;
			}
		}
	}
	//10進数から2進数に変換
	for (int i = 0; i < HEX_NUMBER; ++i) {
		char* tmp = int2bin(ints[i]);
		for (int c = 0; c < 4; ++c) {
			*bits++ = tmp[c];
		}
	}
}

void calc_error_detection(char* bits, char* error) {

	char result_bits[BIT_NUMBER];

	for (int i = 0; i < BIT_NUMBER; ++i) result_bits[i] = bits[i];

	for (int divisor_target = 0; divisor_target < BIT_NUMBER - 4; ++divisor_target) {

		if (result_bits[divisor_target] == '0') continue;

		for (int i = 0; i < BIT_NUMBER; ++i) {
			if (i >= divisor_target && i < divisor_target + 5) {
				if (result_bits[i] == DIVISOR[i - divisor_target])
					result_bits[i] = '0';
				else
					result_bits[i] = '1';
			}
		}
	}

	for (int i = 0; i < 4; ++i) error[i] = result_bits[BIT_NUMBER - 4 + i];
}


void add_error_detection(char* bits) {

	char error_detection[4];

	calc_error_detection(bits, error_detection);

	for (int i = 0; i < 4; ++i) bits[BIT_NUMBER + i] = error_detection[i];
}

void generate_ir_data(unsigned int* rawData, char* bits, int* times) {
	*rawData++ = times[0];
	*rawData++ = times[1];
	for (int i = 0; i < BIT_NUMBER + 4; ++i) {
		*rawData++ = times[2];
		if (bits[i] == '0')
			*rawData++ = times[3];
		else
			*rawData++ = times[4];
	}
	*rawData = times[2];
}

void aircon_data(char* hexs, unsigned int  *rawData) {
	//printf("%d\n", (int)strlen(hexs));
	static char bits[BIT_NUMBER + 4];
	int times[] = {3750, 2050, 300, 600, 1600};
	convert(hexs, bits);
	add_error_detection(bits);
	generate_ir_data(rawData, bits, times);
}

int main(int argc, char const *argv[]) {

	unsigned int  rawData[211];

	aircon_data("aaa5fc0110112200800a004e1", rawData);

	for (int i = 0; i < 211; ++i) {
		printf("%d,", rawData[i] );
	}

	return 0;
}