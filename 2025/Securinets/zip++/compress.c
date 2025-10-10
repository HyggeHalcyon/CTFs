#include <stddef.h>
#include <stdint.h>

int compress_safe(const char *in, size_t in_len, char *out, size_t out_max) {
    if (!in || !out) return -1;
    if (in_len == 0) return 0;          // nothing to do

    uint8_t run = (uint8_t)in[0];
    size_t count = 1;
    size_t in_i = 1;
    size_t out_i = 0;

    while (in_i < in_len) {
        // count repeats up to 255
        while (count < 0xFF && in_i < in_len && (uint8_t)in[in_i] == run) {
            ++count;
            ++in_i;
        }

        // ensure space for two bytes
        if (out_i + 2 > out_max) return -2; // output buffer too small

        out[out_i++] = (char)run;
        out[out_i++] = (char)count;

        // if we've reached end of input, break
        if (in_i >= in_len) break;

        // start new run with next char
        run = (uint8_t)in[in_i++];
        count = 1;
    }

    return (int)out_i; // bytes written (>=0)
}
