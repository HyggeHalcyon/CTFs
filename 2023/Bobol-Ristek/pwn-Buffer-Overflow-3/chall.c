#include <stdio.h>

void target() {
    puts("this_string_is_replaced_by_a_flag_on_the_server");
}

void run() {
    char buf[10];
    gets(buf);
    puts("Noted!");
}

int main(int argc, char const *argv[])
{
    setvbuf(stdout, NULL, _IONBF, 0);
    puts("What do you want?");
    run();
    return 0;
}