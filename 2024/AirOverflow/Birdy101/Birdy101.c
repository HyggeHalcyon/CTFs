// Compile: gcc -o canary101 canary101.c -no-pie -lpthread

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>

__attribute__((constructor))
void __constructor__(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    signal(SIGALRM, exit);
    alarm(0x20);
}

void notepad() {
    char buffer[0x100];
    printf("[Under construction] - This section is underconstruction and only allows a single note to be kept in memory\nEnter the contents you want to store: ");
    if(read(STDIN_FILENO, buffer, 0x1000) < 0) {
        fprintf(stderr, "Unable to read the contents of your note. :(");
        exit(1);
    }
    printf("Thank you for storing the note.\n");
}

void register_user() {
    const int SZ = 256;
    char default_user[] = "DEFAULT";
    char buffer[SZ];
    char *name = buffer;
    memset(name, 0x0, SZ);
    printf("What is your name? ");
    if(read(STDIN_FILENO, &name, SZ-1) < 0) {
        name = default_user;
    }
    printf("Welcome %s\n", name);
}

void vuln() {
    pthread_t pt;
    if(pthread_create(&pt, NULL, (void*)notepad, NULL) < 0) {
        fprintf(stderr, "Unable to spawn a new thread. Something's wrong. Please check!");
        exit(1);
    }
    if(pthread_join(pt, NULL) != 0){
        fprintf(stderr, "Well, something's messed up.");
    }
}

int main(int argc, char* argv[], char* envp[]) {
    register_user();
    vuln();
    return 0;
}