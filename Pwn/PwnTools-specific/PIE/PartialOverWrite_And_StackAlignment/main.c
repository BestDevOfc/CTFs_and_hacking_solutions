#include <stdio.h>
#include <stdlib.h>

void vuln() {
	printf("Take a slice of pie...\n");
	char buffer[8];
	read(0, buffer, 64);
}

void win() {
	system("cat flag.txt");
}

int main() {
	vuln();
	return 0;
}