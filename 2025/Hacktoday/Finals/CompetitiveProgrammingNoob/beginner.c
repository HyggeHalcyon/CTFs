#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int win = 0;

void swap(double *a, double *b) {
  double c = *a;
  *a = *b;
  *b = c;
}

int main() {
  ++win;
  if (win == 2) {
    char buf[100];
    FILE *fd = fopen("./flag.txt", "r");
    if (fd == 0) {
        printf("flag.txt not found\n");
        exit(-1);
    }
    fgets(buf, sizeof(buf), fd);
    fclose(fd);
    printf("Wow, you are a really good guesser!\n");
    printf("Here's the flag:\n%s\n", buf);
    exit(0);
  }

  double array[100] = {0};
  long bucket[1000] = {0};
  double temp;
  for (int i = 0; i < 100; ++i) {
    scanf("%lf", &temp);
    if (temp < 0) {
      printf("Not allowed to be minus\n");
      --i;
      continue;
    }

    if (temp < 1000)
      bucket[(int)temp]++;
      array[i] = temp;
      for (int j = i; j >= 0; --j) {
        if (array[j] < array[j-1]) {
          swap(&array[j], &array[j-1]);
        }
      }
  }

  printf("The number under 1000 with the most occurences is %lf\n", array[99]);
  printf("with %ld occurences\n", bucket[(int)array[99]]);
  
  int count = 0;
  for (int i = 0; i < 100; ++i) {
    if (array[i] == array[99]) ++count;
  }
  bucket[(int)array[99]] -= count;
  //printf("%d\n", bucket[(int)array[99]]);
}
