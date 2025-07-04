// gcc chal.c -o chal

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <sys/mman.h>

void win(int sig) {
  puts("Well done!");
  system("cat ./flag*");
  exit(0);
}

int main() {
  // If you cause SEGV, then you will get flag
  signal(SIGSEGV, win);
  setbuf(stdout, NULL);

  while (1) {
    unsigned int size = 100;
    
    printf("Enter size: ");
    scanf("%u%*c", &size);
    
    char *buf = mmap(NULL, size, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    if (!buf) {
      puts("Too large!");
      exit(1);
    }
    
    printf("Input: ");
    fgets(buf, size, stdin);
    buf[strcspn(buf, "\n")] = '\0';
    
    printf("Your string length: %d\n", strlen(buf));
  }
}
