

#include<stdio.h>
#include<stdlib.h>
#include<string.h>

int main(int argc, char *argv[])
{
    setvbuf(stdout, NULL, _IONBF, 0);
    int hack_me = 0x1;
    char buf[10]; 
    puts("Enter your name (Max 10 characters)");
    gets(buf);

    if(hack_me == 0x12345678)
        system("echo \"Hi, here is your flag\"; cat flag.txt");
    else
        puts("Ok thanks");
    return 0;
}
