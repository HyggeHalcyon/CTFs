//
// https://github.com/elzoughby/Base64
//

#include "base64.h"

char base64_map[] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                     'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
                     'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                     'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/'};


char* base64_encode(char* plain) {

    char counts = 0;
    char buffer[3];
    char* cipher = malloc(strlen(plain) * 4 / 3 + 4);
    int i = 0, c = 0;

    for(i = 0; plain[i] != '\0'; i++) {
        buffer[counts++] = plain[i];
        if(counts == 3) {
            cipher[c++] = base64_map[buffer[0] >> 2];
            cipher[c++] = base64_map[((buffer[0] & 0x03) << 4) + (buffer[1] >> 4)];
            cipher[c++] = base64_map[((buffer[1] & 0x0f) << 2) + (buffer[2] >> 6)];
            cipher[c++] = base64_map[buffer[2] & 0x3f];
            counts = 0;
        }
    }

    if(counts > 0) {
        cipher[c++] = base64_map[buffer[0] >> 2];
        if(counts == 1) {
            cipher[c++] = base64_map[(buffer[0] & 0x03) << 4];
            cipher[c++] = '=';
        } else {                      // if counts == 2
            cipher[c++] = base64_map[((buffer[0] & 0x03) << 4) + (buffer[1] >> 4)];
            cipher[c++] = base64_map[(buffer[1] & 0x0f) << 2];
        }
        cipher[c++] = '=';
    }

    cipher[c] = '\0';   /* string padding character */
    return cipher;
}