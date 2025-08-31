#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <seccomp.h>

#define STORAGE_SIZE 3
#define MAX_DESC_LEN 0x38

char *evidences[STORAGE_SIZE];

void setup_seccomp(void) {
    scmp_filter_ctx ctx;

    ctx = seccomp_init(SCMP_ACT_ALLOW);
    if (ctx == NULL) {
        perror("seccomp_init");
        exit(EXIT_FAILURE);
    }

    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execve), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execveat), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(fork), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(vfork), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(clone), 0);

    if (seccomp_load(ctx) != 0) {
        perror("seccomp_load");
        seccomp_release(ctx);
        exit(EXIT_FAILURE);
    }
    seccomp_release(ctx);
}

void setup(void) {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    setup_seccomp();
}

int main(void) {
    setup();

    puts("Good morning, detective!");
    puts("Somebody has stolen the prized possession of the sacred village!");
    puts("We need your help to gather all the evidence you can to catch this thief!");

    int choice = 0, index = -1;
    size_t size = -1;
    while (1) {
        puts("1. Add evidence");
        puts("2. View evidence");
        puts("3. Remove evidence");
        puts("4. Finish");
        printf("> ");

        scanf("%d%*c", &choice);
        switch (choice) {
        case 1:
            printf("Put into which backpack slot?\n> ");
            scanf("%d%*c", &index);
            if (index < 0 || index >= STORAGE_SIZE) {
                printf("Your backpack only has %d slots!\n", STORAGE_SIZE);
                break;
            }

            printf("How long is the evidence's description?\n> ");
            scanf("%zu%*c", &size);
            if (size > MAX_DESC_LEN) {
                puts("Description too long!");
                break;
            }

            char *evidence = malloc(size);

            printf("Describe the evidence\n> ");
            int len = read(0, evidence, size + 1);
            evidence[len] = '\0';

            evidences[index] = evidence;
            puts("New evidence added!");
            break;
        case 2:
            printf("View which backpack slot?\n> ");
            scanf("%d%*c", &index);
            if (index < 0 || index >= STORAGE_SIZE) {
                printf("Your backpack only has %d slots!\n", STORAGE_SIZE);
                break;
            }
            puts(evidences[index]);
            break;
        case 3:
            printf("Remove which backpack slot?\n> ");
            scanf("%d%*c", &index);
            if (index < 0 || index >= STORAGE_SIZE) {
                printf("Your backpack only has %d slots!\n", STORAGE_SIZE);
                break;
            }
            free(evidences[index]); // UAF
            break;
        case 4:
            puts("Thank you for your work, detective!");
            exit(EXIT_SUCCESS);
            break;
        default:
            puts("Invalid choice");
            break;
        }
    }
}