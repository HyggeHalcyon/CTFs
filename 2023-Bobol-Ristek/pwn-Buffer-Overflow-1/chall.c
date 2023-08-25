

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char const *argv[])
{
	setvbuf(stdout, NULL, _IONBF, 0);
	int hack_me = 0x2;
	char buf[10];

	puts("Enter a number (Max 10 digits)");
	gets(buf);

	if(hack_me > 0x2)
		system("echo \"Hi, here is your flag\"; cat flag.txt");
	else
		puts("Ok thanks");
	return 0;
}
