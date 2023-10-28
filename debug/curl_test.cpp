#include <iostream>
#include <string>
#include <sstream>

using namespace std;

int main(void) {
	string str;
	char c[] = "sample";

	str += "test";
	str += "test";
	str += c;
	cout << str << '\n';

	printf("%s\n",str.c_str() );

	return 0;
}