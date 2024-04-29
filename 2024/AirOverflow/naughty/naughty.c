// Compile: gcc -o naughty naughty.c -fno-stack-protector

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>

#define NAUGHTY_LIST_SZ 0x2
#define MAX_SZ 0x50

__attribute__((constructor))
void __constructor__(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    signal(SIGALRM, exit);
    alarm(0x20);
}

void get_input(int *in) {
    // Secure integer input function.
    // https://stackoverflow.com/questions/41145908/how-to-stop-user-entering-char-as-int-input-in-c
    char next;
    if (scanf("%d", in) < 0 || *in < 0 || ((next = getchar()) != EOF && next != '\n')) {
         clearerr(stdin);
         do next = getchar(); while (next != EOF && next != '\n');
         clearerr(stdin);
    }
}

void ranged_input(int *in, int _beg, int _end) {
    get_input(in);
    while(*in < _beg && *in > _end) {
        printf("Invalid input. Try again: ");
        get_input(in);
    }
}

typedef struct {
    char name[MAX_SZ+1];
    bool is_naughty;
    int already_in;
} child_info_t;

child_info_t naughty_list[NAUGHTY_LIST_SZ];
int written = 0;

int menu() {
    int idx = 0;
    puts("=== Santa's Naughty List ===");
    puts("1. Add a kid to the list");
    puts("2. Print a kid's details");
    puts("3. Fix a kid's name (Elves really can't get the names right)");
    puts("0. Exit");
    printf(">> ");
    ranged_input(&idx, 0, 3);
    return idx;
}

void print_child_info(child_info_t *info) {
    puts("===============");
    printf("Child Info:\nName: ");
    if(!info->already_in) {
        char my_buf[MAX_SZ] = { 0 };
        strncpy(my_buf, info->name, MAX_SZ);
        printf(my_buf);
        info->already_in = true;
    }
    else printf("%s", info->name);
    printf("\nIs child naughty? %s", (info->is_naughty ? "Yes" : "No"));
    puts("\n---------");
}

void init_child(child_info_t info) {
    if(written >= NAUGHTY_LIST_SZ) {
        puts("[ERROR] Too many kids already in the naughty list, can't make it work :(");
        return;
    }
    memset(naughty_list[written].name, NULL, MAX_SZ+1);
    strncpy(naughty_list[written].name, info.name, MAX_SZ);
    naughty_list[written].is_naughty = info.is_naughty;
    naughty_list[written++].already_in = false;
}

void add_kid() {

    if(written >= NAUGHTY_LIST_SZ) {
        puts("[ERROR] Too many kids already in the naughty list, can't make it work :(");
        return;
    }

    char name[MAX_SZ];
    printf("Enter the kid's name: ");
    read(0, name, 0x100);
    child_info_t _kid = {
        .name = name,
        .is_naughty = true,
        .already_in = false
    };
    init_child(_kid);
}

child_info_t* get_child() {
    int idx;
    printf("Enter the child's index: ");
    ranged_input(&idx, 0, NAUGHTY_LIST_SZ-1);
    return &naughty_list[idx];
}

void edit_kid(child_info_t *_kid) {
    if(_kid->already_in) {
        puts("[ERROR] Info has already been modified, cannot modify twice :(");
        return;
    }
    memset(_kid->name, NULL, MAX_SZ);
    printf("Enter new name: ");
    read(0, _kid->name, MAX_SZ);
    printf("Name changed to: %s\n", _kid->name);
}

int main(int argc, char* argv[]) {

    for(int i = 0; i < NAUGHTY_LIST_SZ; i++) {
        child_info_t child = {
            .name = "naughty-kid",
            .is_naughty = true,
            .already_in = false
        };
        init_child(child);
    }

    int choice;
    while(1) {
        choice = menu();
        switch (choice) {
        case 1:
            add_kid();
            break;
        case 2:
            print_child_info(get_child());
            break;
        case 3:
            edit_kid(get_child());
            break;
        case 0:
            puts("Santa Claus is happy, knowing you helped him.");
            exit(0);
        default:
            puts("Invalid input. Try again");
            break;
        }
    }
    return 0;
}