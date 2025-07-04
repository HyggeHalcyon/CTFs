#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define MAX_SIZE 300

void init()
{
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

int main()
{
    init();
    bool end = false;
    while (!end)
    {
        int choice;
        printf("1. Take a fortune\n"
               "2. Share a story\n"
               "3. Exit\n"
               "> ");
        scanf("%d%*c", &choice);
        switch (choice)
        {
        case 1:
            system("fortune");
            break;
        case 2: {
            int size;
            printf("Size: ");
            scanf("%d%*c", &size);
            char buf[size % MAX_SIZE];
            printf("Text: ");
            read(0, buf, size);
            write(1, buf, size);
        }
        break;
        case 3: {
            end = true;
        }
        break;
        default:
            printf("Invalid choice\n");
        }
    }
}
