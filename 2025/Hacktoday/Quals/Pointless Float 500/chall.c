#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

void function1() {
  char buf[16];

  printf("Congrats for passing my first challenge, what's your name?\n> ");
  read(0, buf, 25);
  printf("\nOh, hi %s. Nice to meet you\n", buf);
  printf("This is my first year in uni, how 'bout you?\n> ");
  read(0, buf, 25);
}

void function2() {
  long numbers[10];
  int c;

  printf("What's the magic number?\n> ");
  scanf("%f", (float *)&c);
  getchar();
  if (c == 147) function3(numbers);
  
  write(1, "I'm going to give you another chance to\nchange your numbers, what would you like to change it to\n> ", 99);
  read(0, (void *)&numbers[0], 96);
  write(1, "\nHaha just kidding, i'm out of ideas tbh...\n", 44);
}

void function3(long *numbers) {
  char hacker_name[20];

  printf("Wow, i'm impressed you got it this far.\nYou should consider making a hacker name,\nyou know, the cool names hackers give themselves\n> ");
  read(0, hacker_name, 38);

  printf("\nNow for the next part, please give me 10 integers plz\n> ");
  for (int i = 0; i < 10; ++i)
    scanf("%ld", &numbers[i]);
  getchar(); 
}

int main() {
  float random;
  FILE *fd = fopen("/dev/urandom", "r");
  if (fd == 0) {
    printf("failed reading /dev/urandom\n");
    exit(-1);
  }
  fgets((void *)&random, sizeof(random), fd);
  fclose(fd);

  float guess;
  printf("What's your guess, buddy?\n> ");
  scanf("%f", &guess);
  getchar();
  if (!(guess < random || guess > random)) function1();

  float a;
  double b;
  printf("Now, give me two special numbers!\n> ");
  scanf("%f %lf", &a, &b);
  getchar();
  if (a == 0 || b == 0) {
    printf("You're not allowed to input zero!\n");
    exit(0);
  }
  if (strncmp((void *)&a, (void *)&b, 4) == 0) function2();
}

__attribute__((constructor))
void setup(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}
