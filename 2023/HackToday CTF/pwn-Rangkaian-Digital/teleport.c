#include <stdio.h>
#include <unistd.h>
#include <limits.h>
#include <string.h>

char anu[0x3000];

void init() {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
}

void cool_thing3() {
	char buf[8];
	double a, b;
	printf("\nGive me one final pair of special numbers:\n> ");
	scanf("%lf %lf", &a, &b);
	
	if (a == b) {
		printf("Different numbers please!\n");
		return;
	} else if (*(int *)&a != *(int *)&b) {
		printf("Wrong!\n");
		return;
	}
	
	printf("\nHorray! Here's a present for you, if you need it...\n");
	printf("%ld\n", *(long *)(buf+8));
	read(0, buf, 26);
}

void cool_thing2() {
	char buf[32];
	long a, b;
	printf("\nGive me another two special numbers:\n> ");
	scanf("%ld %ld", &a, &b);
	
	if (a == b) {
		printf("Different numbers please!\n");
		return;
	} else if (*(int *)&a != *(float *)&b) {
		printf("Wrong!\n");
		return;
	}
	
	cool_thing3();
	printf("\nWell done hero! What's your name?\n");
	read(0, buf, 64);
}

void cool_thing1() {
	unsigned long a, b;
	printf("Give me two special numbers:\n> ");
	scanf("%lu %lu", &a, &b);
	
	if (a == b) {
		printf("Different numbers please!\n");
		return;
	} else if (a <= INT_MAX || b <= INT_MAX) {
		printf("Too small!\n");
		return;
	} else if (*(int *)&a != *(unsigned int *)&b) {
		printf("Wrong!\n");
		return;
	}
	
	// printf("\nCongrats! Can you explain what's happening here?\n");
	// read(0, anu, 16);
	cool_thing2();
}

char *useless_function() {
	char *hasil = strstr(anu, "y");
	return hasil;
}

int main() {
	init();
	cool_thing1();
}
