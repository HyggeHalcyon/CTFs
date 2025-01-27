#include <stdio.h>
#include <string.h>
#include <stdbool.h>

bool check(const char* str) {
    int len = strlen(str);
    for (int i = 0; i < len/2; i++) {
        if (str[i] != str[len-1-i]) {
            return false;
        }
    }
    return true;
}

int main() {
    char input[100];
    int len;
    bool valid = true;
    
    scanf("%s", input);
    len = strlen(input);
    
    // Check if string is palindrome
    valid = valid && check(input);
    if (!valid) {
        puts("Wrong 1");
        return 0;
    }
    
    // Check if length is 21 (0x15)
    valid = valid && (len == 21);
    if (!valid) {
        puts("Wrong 2");
        return 0;
    }
    
    // Check for 'a' characters at specific positions
    valid = valid && (len > 20 && 
                     input[0] == 'a' && 
                     input[2] == 'a' && 
                     input[4] == 'a' && 
                     input[7] == 'a' && 
                     input[9] == 'a');
    if (!valid) {
        puts("Wrong 3");
        return 0;
    }
    
    // Check relationship between characters
    valid = valid && (len > 3 && 
                     input[1] == (input[3] - 1));
    if (!valid) {
        puts("Wrong 4");
        return 0;
    }

    
    // Check for 'm' at specific position
    valid = valid && (len > 19 && 
                     input[19] == 'm');
    if (!valid) {
        puts("Wrong 5");
        return 0;
    }
    
    
    // Check for 'p' at specific position
    valid = valid && (len > 15 && 
                     input[15] == 'p');
    if (!valid) {
        puts("Wrong 6");
        return 0;
    }
    
    // Check relationship between characters
    valid = valid && (len > 6 && 
                     input[6] == (input[5] - 4));
    if (!valid) {
        puts("Wrong 7");
        return 0;
    }
    
    // Check if characters at specific positions are equal
    valid = valid && (len > 17 && 
                     input[8] == input[17]);
    if (!valid) {
        puts("Wrong 8");
        return 0;
    }
    
    // Check for 'c' at specific position
    valid = valid && (len > 10 && 
                     input[10] == 'c');
    if (!valid) {
        puts("Wrong 9");
        return 0;
    }
    
    if (valid) {
        printf("%s\n", input);
    } else {
        puts("Wrong!");
    }
    
    return 0;
}
