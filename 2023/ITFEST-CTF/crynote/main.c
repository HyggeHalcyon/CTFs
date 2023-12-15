#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <ctype.h>

struct crynotes {
    void (*func)();
    char *data;
    char *key;
};

struct crynotes *cry[10];
int count = 0;

void input(char *buf, int size){
    int recv, i = 0;
    while(i < size){
        if((recv = (int)read(0, &buf[i], 1)) < 0)
            exit(1);

        if(buf[i] == '\n'){
            buf[i] = '\0';
            break;
        } i++;
    }
}

void cipher(char *data, char *key){

    if(data != NULL && key != NULL){
        size_t datalen = strlen(data);
        size_t keylen = strlen(key);

        for (size_t i = 0; i < datalen; i++) {
            char enc = data[i];

            if(isalpha(enc)){
                char base_data = islower(enc) ? 'a' : 'A';
                char base_key = islower(key[i % keylen]) ?  'a' : 'A';
                enc = (char)(((enc - base_data + key[i % keylen] - base_key) % 26) + base_data);
            }
            enc ^= key[i % keylen];
            printf("%02hhx", enc);
        }
    }
}

void create(){
    int size;

    if(count > 10){
        puts("FULL!");
        return;

    } else { 
        if(!cry[count]){
            
            if(!(cry[count] = (struct crynotes*)malloc(sizeof(struct crynotes))))
                exit(1);

            cry[count]->func = cipher;

            printf("size: ");
            if(!scanf("%d%*c", &size))
                exit(1);

            if(!((cry[count]->data = (char*)malloc(size)) && (cry[count]->key = (char*)malloc(size))))
                exit(1);

            printf("data: ");
            input(cry[count]->data, size);
            
            printf("key: ");
            input(cry[count]->key, size);

	    puts("[+] created");
            count++;
        }
    }
}

void encrypt(){
    int idx;

    printf("index: ");
    if(!scanf("%d%*c", &idx))
        exit(1);

    if(idx < 0 || idx >= count){
        puts("invalid index");
        return;
    }

    if(cry[idx]){
        printf("ciphertext (hex): ");
        cry[idx]->func(cry[idx]->data, cry[idx]->key);
        putchar(10);
    }
}

void delete(){
    int idx;

    printf("index: ");
    if(!scanf("%d%*c", &idx))
        exit(1);

    if(idx < 0 || idx >= count){
        puts("invalid index");
        return;
    }

    if(cry[idx]){
        free(cry[idx]->data);
        free(cry[idx]->key);
        free(cry[idx]);
        puts("[+] deleted");
    }
}

int main(){
    int choice;
    for(;;){
        printf("\n1. create\n"
               "2. encrypt\n"
               "3. delete\n"
               "4. exit\n"
               "> "
                );
        if(!scanf("%d%*c", &choice)){
            puts("Error");
            exit(1);
        }

        switch (choice) {
        case 1:
            create();
            break;
        case 2:
            encrypt();
            break;
        case 3:
            delete();
            break;
        case 4:
            puts("bye!");
            exit(0);
        default:
            puts("invalid choice");
            break;
        }
    }
}

__attribute__((constructor))
void setup(void){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}
