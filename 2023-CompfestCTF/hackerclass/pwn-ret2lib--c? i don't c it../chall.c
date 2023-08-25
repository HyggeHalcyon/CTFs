#include <stdio.h>

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    char buf[1];
    printf("well, just bof me, i don't care anymore :(\n> ");
    gets(buf);
}