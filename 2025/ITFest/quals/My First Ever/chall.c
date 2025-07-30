#include <stdio.h>

int main() {
  char buf[8];
  gets(buf);
  fclose(stdin);
  fclose(stdout);
  fclose(stderr);
}

__attribute__((constructor))
void setup(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}
