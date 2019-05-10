#include <stdio.h>

#define BIT_NUMBER 25
/*

16進数のコードから
２進数変換
誤り検知符号
raw_data変換

*/

char *int2bin(int x) {
	static char bin[4];
	for (int i = 0; i < 4; ++i) {
		bin[i] = ((x >> i) & 1 ) + '0';
	}
	return bin;
}

void convert(char *hexs, char *bits) {
	char table[] = "0123456789abcdef";
	int ints[BIT_NUMBER];

	printf("%s\n", hexs );

	//16進数から10進数に変換
	for (int i = 0; i < BIT_NUMBER; ++i) {
		for (int t = 0; t < 16; ++t) {
			if (hexs[i] == table[t]) {
				ints[i] = t;
				break;
			}
		}
	}
	//10進数から２進数に変換
	for (int i = 0; i < BIT_NUMBER; ++i) {
		char *tmp = int2bin(ints[i]);
		for (int c = 0; c < 4; ++c) {
			*bits = tmp[c];
			++bits;
		}
	}
}


int main(int argc, char const *argv[]) {
	static char bits[BIT_NUMBER];
	convert("aaa5fc0110112200800a004e1", bits);
	printf("%s\n", bits );
	return 0;
}