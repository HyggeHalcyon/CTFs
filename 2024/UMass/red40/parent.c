#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
#include <time.h>

#include <sys/types.h>
#include <signal.h>

void setup()
{
    srand(time(NULL));
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

void forker()
{
    int pid = fork();
    if (pid == 0)
    {
        char *nargv[] = {"red40", "loop", (char *)0};
        char *nenv[] = {NULL};
        execve("red40", nargv, NULL);
    }
    else
    {
        char *flag = malloc(0x30);

        strncpy(flag, "UMASS{TEST_FLAG}", 0x30);
        waitpid(pid, NULL, 0);
    }
}

int main(int argc, char *argv[])
{
    setup();

    int r = rand() % (500 + 100);
    for (int i = 0; i < r; i++)
    {
        int pid = fork();
        if (pid == 0)
        {
        }
        else
        {
            kill(pid, SIGKILL);
            waitpid(pid, NULL, 0);
        }
    }

    if (argc == 2)
    {
        if (!strncmp(argv[1], "fork", 4))
            forker();
    }
    else
    {
        int pid = fork();
        if (pid == 0)
        {
            char *nargv[] = {"parent", "fork", (char *)0};
            char *nenv[] = {NULL};
            execve("parent", nargv, NULL);
        }
        else
        {
            waitpid(pid, NULL, 0);
        }
    }
}