#include <stdio.h>

#define BIT_NUMBER 25
/*

16進数のコードから
２進数変換
誤り検知符号
raw_data変換

*/

char *int2bin(int x) {
	static char bin[5];
	for (int i = 0; i < 4; ++i) {
		bin[i] = ((x >> i) & 1 ) + '0';
	}
	printf("%s\n", bin );
	return bin;
}

int* convert(char *hexs) {

	for (int i = 0; i < BIT_NUMBER; ++i) {
		printf("%c", hexs[i] );
	}
	printf("\n");

	int* bits;
	char table[] = "0123456789abcdef";
	int ints[BIT_NUMBER];

	for (int i = 0; i < BIT_NUMBER; ++i) {
		for (int t = 0; t < 16; ++t) {
			if (hexs[i] == table[t]) {
				ints[i] = t;
				break;
			}
		}
	}

	for (int i = 0; i < BIT_NUMBER; ++i) {
		int target_int = ints[i];
		int2bin(target_int);
	}
	return bits;
}


int main(int argc, char const *argv[]) {
	convert("aaa5fc0110112200800a004e1");
	//int2bin(15);
	return 0;
}