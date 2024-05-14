#include<stdlib.h>
#include<stdio.h>

int main(){
    char a;
    a = system("cat f*");
    printf("%s",a);
}