#include <stdio.h>
#include <stdlib.h>

#define BUF_SIZE 0x100

__attribute__((constructor)) _()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    puts("Selamat datang para peserta CTF COMPFEST 16!");
    puts("Sebelum tahap penyisihan, kami ingin mengetahui harapan Anda sebagai peserta kami.");
    puts("Silakan isi form berikut dengan harapan Anda. Terima kasih!");
}

void read_val(const char *msg, void *ptr)
{
    printf("%s", msg);
    scanf("%ld", ptr);
}

int main()
{
    puts("\n===== Form Harapan Peserta CTF COMPFEST 16 =====");

    int key = 0;
    int length;
    read_val("Panjang harapan (biar efisien harap maklum): ", &length);
    if (length < 0 || length >= BUF_SIZE)
    {
        printf("Hayo jangan nackal ya dek...\n");
        return -1;
    }

    if (key == 0xDEADBEEF)
    {
        puts("\nEmang boleh se-hengker ini...");
        system("/bin/sh");
        return 69;
    }

    puts("Mohon maaf saat ini form sedang dalam perbaikan. Silakan coba chall sebelah dulu hehe.");
}
