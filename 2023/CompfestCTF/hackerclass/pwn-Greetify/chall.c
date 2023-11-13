#include <stdio.h>

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);

    char file_to_open[] = "hello_there.txt";

    puts("Welcome to Greetify! ^^");
    puts("We are here to greet you, hope you enjoy our company! :D");
    printf("First off, what is your name? ");

    char name[88];
    gets(name);

    FILE *fptr = fopen((char *)file_to_open, "r");
    if (fptr == NULL) {
        printf("File %s does not exist! >:(", file_to_open);
        return 69;
    }

    char* hello;
    fscanf(fptr, "%s", hello);
    puts("");
    printf("%s %s\n", hello, name);

    puts("Fin. Thank you for using Greetify! ^^");
    fclose(fptr);
}