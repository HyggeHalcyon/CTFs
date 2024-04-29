// Compile: gcc -o partial partial.c -fPIC -fno-stack-protector

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <unistd.h>

__attribute__((constructor))
void __constructor__(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    signal(SIGALRM, exit);
    alarm(0x20);
}

const char *GUEST_ROLE = "guest";
const char *ADMIN_ROLE = "admin";

typedef struct {
    char name[50];
    char *role;
} userProfile;
userProfile *p;

int menu() {
    int choice;
    puts("== Menu ==");
    puts("1. Set name");
    puts("2. Set role");
    puts("3. Show profile");
    puts("4. Access secret area");
    puts("0. Exit");
    printf("> ");
    scanf("%d", &choice);
    return choice;
}

void set_name() {
    char name[50];
    printf("Enter your name: ");
    if(p->name[0] == '\0') {
        return read(STDIN_FILENO, p->name, 0x100);
    }
    read(STDIN_FILENO, name, 0x100);
    strncpy(p->name, name, 0x100);
}

void set_role() {
    puts("Due to recent breaches. Users can't change their roles. However, if you don't have a role, you'll be assigned guest!");
    if (p->role == NULL) {
        p->role = GUEST_ROLE;
    }
}

void show_profile() {
    printf("Name: %s\n", p->name);
    printf("Role: %s\n", p->role);
}

int main() {

    p = malloc(sizeof(userProfile));
    p->role = NULL;
    memset(p->name, 0, 50);

    while (1) {
        switch (menu()) {
            case 1:
                set_name();
                break;
            case 2:
                set_role();
                break;
            case 3:
                show_profile();
                break;
            case 4:
                if (p->role == ADMIN_ROLE) {
                    puts("Welcome admin!");
                    puts("[UNIMPLEMENTED] - This is an unimplemented feature :(");
                } else {
                    puts("You're not an admin!");
                }
                break;
            case 0:
                return 0;
            default:
                puts("Invalid choice!");
                break;
        }
    }
    return 0;

}
