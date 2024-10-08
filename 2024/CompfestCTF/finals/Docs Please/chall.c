#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdlib.h>

static const char base64_table[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

void base64_decode(const char *input, char *output) {
    int len = strlen(input);
    int i, j = 0, k = 0;
    unsigned char buf[4];
    unsigned char tmp[3];

    for (i = 0; i < len; i++) {
        if (input[i] == '=') {
            break;
        }

        for (j = 0; j < 64; j++) {
            if (input[i] == base64_table[j]) {
                buf[k++] = j;
                break;
            }
        }

        if (k == 4) {
            tmp[0] = (buf[0] << 2) | (buf[1] >> 4);
            tmp[1] = (buf[1] << 4) | (buf[2] >> 2);
            tmp[2] = (buf[2] << 6) | buf[3];
            for (j = 0; j < 3; j++) {
                *output++ = tmp[j];
            }
            k = 0;
        }
    }

    if (k) {
        if (k == 2) {
            tmp[0] = (buf[0] << 2) | (buf[1] >> 4);
            *output++ = tmp[0];
        } else if (k == 3) {
            tmp[0] = (buf[0] << 2) | (buf[1] >> 4);
            tmp[1] = (buf[1] << 4) | (buf[2] >> 2);
            *output++ = tmp[0];
            *output++ = tmp[1];
        }
    }

    *output = '\0';
}

void remove_rust_comments(const char *code, char *cleaned_code) {
    bool in_block_comment = false;
    bool in_line_comment = false;
    const char *p = code;
    char *out = cleaned_code;

    while (*p != '\0') {
        if (in_block_comment) {
            if (*p == '*' && *(p + 1) == '/') {
                in_block_comment = false;
                p++;
            }
        } else if (in_line_comment) {
            if (*p == '\n') {
                in_line_comment = false;
            }
        } else {
            if (*p == '/') {
                if (*(p + 1) == '*') {
                    in_block_comment = true;
                    p++;
                } else if (*(p + 1) == '/') {
                    in_line_comment = true;
                    p++;
                } else {
                    *out++ = *p;
                }
            } else {
                *out++ = *p;
            }
        }
        p++;
    }
    *out = '\0';
}

void execute_rust_commands(const char *decoded_B) {
    char temp_dir[100];
    
    FILE *fp = popen("mktemp -d", "r");
    if (fp == NULL) {
        printf("Failed to create temp directory\n");
        return;
    }
    
    fgets(temp_dir, sizeof(temp_dir), fp);
    pclose(fp);

    temp_dir[strcspn(temp_dir, "\n")] = 0;

    char cmd[200];
    snprintf(cmd, sizeof(cmd), "cp -r flag-validator %s", temp_dir);
    
    system(cmd);

    char file_path[200];
    snprintf(file_path, sizeof(file_path), "%s/flag-validator/src/lib.rs", temp_dir);
    
    FILE *file_ptr = fopen(file_path, "w");
    if (file_ptr != NULL) {
        fputs(decoded_B, file_ptr);
        fclose(file_ptr);
    } else {
        printf("An error has occured, you may contact the staffs.\n");
        return;
    }

    snprintf(cmd, sizeof(cmd), "cd %s/flag-validator && cargo test", temp_dir);
    
    FILE *cmd_output = popen(cmd, "r");
    if (cmd_output == NULL) {
        printf("Failed to run cargo test.\n");
        return;
    }

    char output[1024];
    while (fgets(output, sizeof(output), cmd_output) != NULL) {
        printf("%s", output);
    }

    pclose(cmd_output);
}

bool compare_code(const char *code1, const char *code2) {
    return strcmp(code1, code2) == 0;
}

bool contains_backtick_or_tilde(const char *code) {
    for (int i = 0; i < strlen(code); i++) {
        if (code[i] == '`' || code[i] == '~') {
            return true;
        }
    }
    return false;
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    const char *base64_encoded_A = "dXNlIHN0ZDo6aW86OlJlYWQ7CnVzZSByZWdleDo6UmVnZXg7CnVzZSBzaGEyOjp7U2hhMjU2LCBEaWdlc3R9OwoKI1thbGxvdyhkZWFkX2NvZGUpXQpmbiB2YWxpZGF0ZV9mbGFnKGZsYWc6ICZzdHIpIC0+IGJvb2wgewogICAgbGV0IGZsYWdfcGF0dGVybiA9IFJlZ2V4OjpuZXcociJeQ09NUEZFU1QxNlx7LipcfSQiKS51bndyYXAoKTsKICAgIGlmICFmbGFnX3BhdHRlcm4uaXNfbWF0Y2goZmxhZykgewogICAgICAgIHByaW50bG4hKCIxIik7CiAgICAgICAgcmV0dXJuIGZhbHNlOwogICAgfQoKICAgIGxldCBmbGFnX2xlbiA9IGZsYWcubGVuKCk7CiAgICBpZiBmbGFnX2xlbiA8IDEyIHsKICAgICAgICBwcmludGxuISgiMiIpOwogICAgICAgIHJldHVybiBmYWxzZTsKICAgIH0KCiAgICBsZXQgbGFzdF8xMF9jaGFycyA9ICZmbGFnW2ZsYWdfbGVuIC0gMTEuLmZsYWdfbGVuIC0gMV07CgogICAgbGV0IGNvbnRlbnRfc3RhcnQgPSBmbGFnLmZpbmQoJ3snKS51bndyYXAoKSArIDE7CiAgICBsZXQgY29udGVudF9lbmQgPSBmbGFnX2xlbiAtIDEyOwogICAgbGV0IGNvbnRlbnRfYmVmb3JlX2xhc3RfMTAgPSAmZmxhZ1tjb250ZW50X3N0YXJ0Li5jb250ZW50X2VuZF07CgogICAgbGV0IG11dCBoYXNoZXIgPSBTaGEyNTY6Om5ldygpOwogICAgaGFzaGVyLnVwZGF0ZShjb250ZW50X2JlZm9yZV9sYXN0XzEwKTsKICAgIGxldCByZXN1bHQgPSBoYXNoZXIuZmluYWxpemUoKTsKCiAgICBsZXQgaGFzaGVkX3N0cmluZyA9IGZvcm1hdCEoIns6eH0iLCByZXN1bHQpOwogICAgbGV0IGZpcnN0XzEwX2hhc2hlZF9jaGFycyA9ICZoYXNoZWRfc3RyaW5nWy4uMTBdOwoKICAgIGxhc3RfMTBfY2hhcnMgPT0gZmlyc3RfMTBfaGFzaGVkX2NoYXJzCn0KCiNbY2ZnKHRlc3QpXQptb2QgdGVzdHMgewogICAgdXNlIHN1cGVyOjoqOwogICAgY29uc3QgUEFUSF9UT19GTEFHOiAmc3RyID0gInJlc291cmNlcy9mbGFnLnR4dCI7CgogICAgI1t0ZXN0XQogICAgZm4gdGVzdF92YWxpZF9mbGFnKCkgewogICAgICAgIGxldCBtdXQgZmlsZV9vcGVuID0gc3RkOjpmczo6RmlsZTo6b3BlbihQQVRIX1RPX0ZMQUcpLmV4cGVjdCgiRmxhZyBmaWxlIG5vdCBmb3VuZC4iKTsKICAgICAgICBsZXQgbXV0IGZsYWdfc3RyaW5nID0gU3RyaW5nOjpuZXcoKTsKICAgICAgICBmaWxlX29wZW4ucmVhZF90b19zdHJpbmcoJm11dCBmbGFnX3N0cmluZykuZXhwZWN0KCJGaWxlIGNhbid0IGJlIHJlYWQiKTsKICAgICAgICBhc3NlcnQhKHZhbGlkYXRlX2ZsYWcoJmZsYWdfc3RyaW5nKSk7CiAgICB9Cn0KCg==";

    printf("Can you help me write documentation for my library :)\n");
    printf("Rules:\n");
    printf("1. Docs ONLY! No hacking >:(\n");
    printf("2. You may write docs on a newline separated from the code\n\n");
    printf("Here's my lib.rs in base64 encoding:\n%s\n", base64_encoded_A);

    char base64_encoded_B[4096];
    printf("Submit the documented version of the code (base64):\n");
    scanf("%s", base64_encoded_B);

    char decoded_A[2048];
    char decoded_B[2048];
    char cleaned_B[2048];

    base64_decode(base64_encoded_A, decoded_A);
    base64_decode(base64_encoded_B, decoded_B);

    remove_rust_comments(decoded_B, cleaned_B);

    // printf("%s", cleaned_B);

    printf("DECODED A:\n %s\n", decoded_A);
    printf("CLEANED B:\n %s\n", cleaned_B);
    if (!compare_code(decoded_A, cleaned_B)) {
        printf("\nATTN: cmp code!!\n");
	    return 0;
    }

    if (contains_backtick_or_tilde(cleaned_B)) {
        printf("ATTN: bad chars!!\n");
        return 0;
    }

    printf("Thanks!, we'll run the test suite just to be safe :D\n");

    execute_rust_commands(decoded_B);

    return 0;
}

