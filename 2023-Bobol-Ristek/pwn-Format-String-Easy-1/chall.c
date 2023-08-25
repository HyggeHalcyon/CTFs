#include <stdio.h>
#include <stdlib.h>

int main(int argc, char const *argv[]) {
	setvbuf(stdout, NULL, _IONBF, 0);
	int hack_me = 0x5;
	char buf[16];

	puts("Enter a number (Max 10 digits)");
	scanf("%10s", buf);

	printf("Your input, hack_me: ");
	printf(buf, &hack_me);
	printf("\n");

	if(hack_me > 0x5)
		system("echo \"Hi, here is your flag\"; cat flag.txt");
	else
		puts("Ok thanks");
	return 0;
}
