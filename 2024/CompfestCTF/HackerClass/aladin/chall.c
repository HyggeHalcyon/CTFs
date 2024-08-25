#include <stdio.h>
#include <stdlib.h>

/* gcc -Wl,-z,relro,-z,now -no-pie -fno-stack-protector chall.c -o chall */

void win(int mantra)
{
    puts("wow! mantra kamu benar! sebagai hadiahnya, jin akan memberikan kamu suatu mantra lain yang dapat kamu gunakan untuk menang ctf compfest (semoga beneran).");
    FILE *f = fopen("flag.txt", "r");
    if (f == NULL)
    {
        printf("File flag.txt does not exist! >:(");
        return 69;
    }
    char flag[0x100];
    fgets(flag, 0x100, f);
    puts(flag);
}

void vuln()
{
    char mantra[32];

    puts("kamu menemukan sebuah gua... di dalam gua tersebut ada jin yang bisa memberi kamu akses jadi pemenang ctf compfest 16...");
    puts("tapi syaratnya kamu harus bisa menyebutkan mantra sakti yang diinginkan jin tersebut...\n");
    puts("jin: 'tenang saja... soal ini tidak toksik seperti soal tahun lalu... tapi kamu harus menyebutkan mantra sakti...'\n");
    printf("sebutkan mantra sakti tersebut: ");

    read(0, mantra, 0x200);

    puts("duar! jin tersebut memproses mantra sakti kamu... apakah kamu akan jadi pemenang ctf compfest 16...?\n");
}

int main()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    vuln();
    puts("yah, nampaknya mantra kamu masih salah...");
    return 0;
}
