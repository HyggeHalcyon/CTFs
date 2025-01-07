/* --- Only this file is in scope. (If you find a 0day in sqlite you may of course use it ;) --- */

#include <stdio.h>
#include <sqlite3.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <err.h>

#include "base64.h"

#define DEBUG false

enum user_flags {
    permission_create = 1<<1,
    permission_update = 1<<2,
    permission_view = 1<<3,
    permission_list = 1<<4,

    permission_login = 1<<5,
    permission_register = 1<<6,

    permission_root = 1<<8,
};

struct paste {
    int rowId;
    char title[256];
    char language[256];
    char content[256];
};

struct user {
    int userId;
    uint64_t flags;
    char username[256];
    char password[256];
};

int rc;
char* errMsg;
sqlite3 *db;

char admin_password[512];
char line_buffer[512];
struct paste paste;
struct user current_user;

void login_anonymous() {
    current_user.userId = -1;
    current_user.flags = permission_create | permission_update | permission_view | permission_list;
    strcpy(current_user.username, "anonymous");
}

void print_paste(struct paste* paste) {
    printf("===== Paste %d =====\n", paste->rowId);
    printf("Title: %s", paste->title);
    printf("Language: %s", paste->language);
    printf("Content: \n%s", paste->content);
    printf("\n\n");
}

void error_handle(int expect) {
    if (rc != expect) {
        fprintf(stderr, "Sqlite error: %s\n", errMsg ? errMsg : sqlite3_errmsg(db));
        sqlite3_free(errMsg);
        exit(EXIT_FAILURE);
    }
}

bool check_permissions(const int perms) {
    if ((current_user.flags & perms) != perms) {
        printf("You don't have permissions to perform this action!\n");
        if (current_user.userId == -1) {
            printf("You might need to login to unlock this.\n");
        }
        return false;
    }
    return true;
}

void init_admin() {
    FILE* rng = fopen("/dev/urandom", "r");
    if (rng == NULL)
        errx(EXIT_FAILURE, "Failed to open /dev/urandom");
    char* result = fgets(line_buffer, 100 * sizeof(char), rng);
    if (result == NULL)
        errx(EXIT_FAILURE, "Failed to read from /dev/urandom");
    char* pass = base64_encode(line_buffer);
    strcpy(admin_password, pass);
    free(pass);
    if (DEBUG) {
        printf("Generated random admin password: %s\n", admin_password);
    }
}

void action_create();
void action_update();
void action_info();
void action_list();
void action_sys();
void action_login();

int main(void) {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);

    init_admin();
    login_anonymous();

    rc = sqlite3_open("paste.db", &db);
    if (rc) {
        fprintf(stderr, "Sqlite error: %s\n", sqlite3_errmsg(db));
        exit(EXIT_FAILURE);
    }

    rc = sqlite3_exec(db, "CREATE TABLE IF NOT EXISTS entries(user INT, title TEXT, language TEXT, content BLOB)", NULL, 0, &errMsg);
    error_handle(SQLITE_OK);

    do {
        printf(
            "\n===== SQLate =====\n"
            "1) Create new Paste\n"
            "2) Update a Paste\n"
            "3) Show a Paste\n"
            "4) List all Pastes\n"
            "5) Login / Register\n"
            "6) Exit\n"
            "\n"
            "> "
        );

        const int c = fgetc(stdin);
        fgetc(stdin);

        switch (c) {
            case '1': {
                if (!check_permissions(permission_create)) continue;

                action_create();
                continue;
            }
            case '2': {
                if (!check_permissions(permission_update)) continue;

                action_update();
                continue;
            }
            case '3': {
                if (!check_permissions(permission_view)) continue;

                action_info();
                continue;
            }
            case '4': {
                if (!check_permissions(permission_list)) continue;

                action_list();
                continue;
            }
            case '5': {
                printf("Registration is currently closed.\n\n");
                action_login();
                continue;
            }
            case EOF:
            case '6':
                return 0;
            case '7': {
                if (!check_permissions(permission_root)) continue;

                action_sys();
                continue;
            }
            default: {
                printf("Unknown action %c!", c);
            }
        }
    } while(true);
}

void read_to_buffer(const char* description) {
    printf("Enter %s: ", description);
    fgets(line_buffer, 256, stdin);
}

void action_create() {
    const int default_limit = sqlite3_limit(db, SQLITE_LIMIT_LENGTH, 512);

    sqlite3_stmt *stmt;
    rc = sqlite3_prepare_v2(db, "INSERT INTO entries(title, language, content) VALUES(?, ?, ?)", -1, &stmt, 0);

    read_to_buffer("Title");
    rc = sqlite3_bind_text(stmt, 1, line_buffer, -1, SQLITE_TRANSIENT);
    error_handle(SQLITE_OK);

    read_to_buffer("Language");
    rc = sqlite3_bind_text(stmt, 2, line_buffer, -1, SQLITE_TRANSIENT);
    error_handle(SQLITE_OK);

    read_to_buffer("Content");
    rc = sqlite3_bind_text(stmt, 3, line_buffer, -1, SQLITE_TRANSIENT);
    error_handle(SQLITE_OK);

    rc = sqlite3_step(stmt);
    error_handle(SQLITE_DONE);

    rc = sqlite3_finalize(stmt);
    error_handle(SQLITE_OK);

    sqlite3_limit(db, SQLITE_LIMIT_LENGTH, default_limit);
}

void action_update() {
    sqlite3_stmt *stmt;

    printf(
        "Which field?\n"
        "1) Language\n"
        "2) Content\n"
        "\n"
        ">"
    );

    int c = getc(stdin);
    getc(stdin);

    if (c != '1' && c != '2') return;
    const char* field = c == '1' ? "language" : "content";

    if (c == '2') {
        printf(
            "Which modifier?\n"
            "1) None\n"
            "2) Hex\n"
            "3) Base64\n"
            "\n"
            ">"
        );

        c = getc(stdin);
        getc(stdin);

        read_to_buffer(field);

        if (c == '1' || c == '3') {
            rc = sqlite3_prepare_v2(db, "UPDATE entries SET content=? WHERE title = ?", -1, &stmt, 0);
        } else if (c == '2') {
            rc = sqlite3_prepare_v2(db, "UPDATE entries SET content=HEX(?) WHERE title = ?", -1, &stmt, 0);
        } else {
            printf("Invalid choice\n");
            return;
        }

        if (c == '3') {
            char* temp = base64_encode(line_buffer);
            if (strlen(temp) > 255) err(EXIT_FAILURE, "Attempted to overflow!");
            strcpy(line_buffer, temp);
            free(temp);
        } else if (c == '2') {
            if (strlen(line_buffer) > 192) err(EXIT_FAILURE, "Attempted to overflow!");
        }
    } else {
        rc = sqlite3_prepare_v2(db, "UPDATE entries SET language=? WHERE title = ?", -1, &stmt, 0);
    }
    error_handle(SQLITE_OK);

    rc = sqlite3_bind_text(stmt, 1, line_buffer, -1, SQLITE_TRANSIENT);
    error_handle(SQLITE_OK);

    read_to_buffer("Title");
    rc = sqlite3_bind_text(stmt, 2, line_buffer, -1, SQLITE_TRANSIENT);
    error_handle(SQLITE_OK);
    printf("'%s'\n", line_buffer);

    rc = sqlite3_step(stmt);
    error_handle(SQLITE_DONE);
}

void action_info() {
    sqlite3_stmt *stmt;
    rc = sqlite3_prepare_v2(db, "SELECT rowid, title, language, content FROM entries WHERE title = ?", -1, &stmt, 0);
    error_handle(SQLITE_OK);

    read_to_buffer("Title");
    rc = sqlite3_bind_text(stmt, 1, line_buffer, -1, SQLITE_TRANSIENT);
    error_handle(SQLITE_OK);

    rc = sqlite3_step(stmt);
    if (rc == SQLITE_DONE) {
        printf("No paste with that title found!");
        return;
    }
    error_handle(SQLITE_ROW);

    const int rowId = sqlite3_column_int(stmt, 0);
    const char* title = (char*) sqlite3_column_text(stmt, 1);
    const char* language = (char*) sqlite3_column_text(stmt, 2);
    const char* content = (char*) sqlite3_column_text(stmt, 3);

    paste.rowId = rowId;
    strcpy(paste.title, title);
    strcpy(paste.language, language);
    strcpy(paste.content, content);

    print_paste(&paste);

    rc = sqlite3_finalize(stmt);
    error_handle(SQLITE_OK);
}

void action_list() {
    sqlite3_stmt *stmt;
    rc = sqlite3_prepare_v2(db, "SELECT rowid, title, language, content FROM entries", -1, &stmt, 0);
    error_handle(SQLITE_OK);

    rc = sqlite3_step(stmt);
    if (rc == SQLITE_DONE) {
        printf("You don't have any pastes right now.\n");
        return;
    }
    error_handle(SQLITE_ROW);

    while (rc == SQLITE_ROW) {
        const int rowId = sqlite3_column_int(stmt, 0);
        const char* title = (char*) sqlite3_column_text(stmt, 1);
        const char* language = (char*) sqlite3_column_text(stmt, 2);
        const char* content = (char*) sqlite3_column_text(stmt, 3);

        paste.rowId = rowId;
        strcpy(paste.title, title);
        strcpy(paste.language, language);
        strcpy(paste.content, content);

        print_paste(&paste);

        rc = sqlite3_step(stmt);
    }

    rc = sqlite3_finalize(stmt);
    error_handle(SQLITE_OK);
}

void action_sys() {
    system("/usr/bin/cat flag");
}

void action_login() {
    // Currently only admin login
    read_to_buffer("Password?");
    unsigned long length = strlen(line_buffer);
    for (unsigned long i = 0; i < length && i < 512; i++) {
        if (line_buffer[i] != admin_password[i]) {
            printf("Wrong password!\n");
            return;
        }
    }

    strcpy(current_user.username, "admin");
    current_user.userId = 0;
    current_user.flags = 0xFFFFFFFF;
}
