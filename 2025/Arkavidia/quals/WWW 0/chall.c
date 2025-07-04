#include <stdio.h>
#include <stdlib.h>

void gift()
{
    char buf[1024] = {0};
    scanf(" %32[^$n\n]", buf);
    printf(buf);
    putchar('\n');
}

int main()
{
    gift();
    long long *ptr;
    printf("Where: ");
    fflush(stdout);
    scanf("%p", &ptr);
    printf("What: ");
    fflush(stdout);
    scanf("%lli", ptr);
    exit(0);
}
