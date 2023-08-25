#include <stdio.h>

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
}

void vuln() {
    char buf[0x20];
    puts("\ncanary2win e youkoso~ input wo joudai >//<");
    printf("> ");
    gets(buf);
    printf(buf);
}

void win() {
    puts("\nDiff spike gak gan, ngga lah ya xixixi :pray:");
    FILE *f = fopen("flag.txt", "r");
    char buf[0x100];
    fgets(buf, 0x100, f);
    puts(buf);
}

int main() {
    init();
    while(1) vuln();
}