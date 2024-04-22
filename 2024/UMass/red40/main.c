#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <time.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <errno.h>

#include <sys/mman.h>
#include <seccomp.h>

int RED40 = 1000;
int STEAL = 0;
int WARN = 0;

void setup()
{
	srand(time(NULL));
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	setbuf(stderr, NULL);
}

void setupv2()
{
	scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_ALLOW);
	seccomp_rule_add(ctx, SCMP_ACT_KILL_PROCESS, SCMP_SYS(execve), 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL_PROCESS, SCMP_SYS(execveat), 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL_PROCESS, SCMP_SYS(socket), 0);
	seccomp_load(ctx);
}

void print_menu()
{
	puts("What would you like to do with your RED40?");
	puts("1. Appreciate RED40");
	puts("2. Gamble RED40");
	puts("3. Warn RED40");
	puts("4. Consume RED40");
	puts("5. STEAL RED40");
	puts("6. Exit (no RED40 for you)");
}

int getnum()
{
	int d;
	scanf("%d", &d);
	getchar();
	return d;
}

void appreciate()
{
	printf("You are now appreciating your %d RED40!\n", RED40);
}

void gamble()
{
	puts("ITS TIME TO GAMBLE RED40!!!");

	int r;
	char again[2];

	while (1)
	{
		puts("Are you ready to gamble??? (\"99.9999999% of gamblers quit right before winning big...\" - Royce du Pont) (Y)");
		printf("\n> ");

		read(0, again, 2);
		again[1] = '\0';

		if (strncmp(again, "Y\0", sizeof(again)))
			break;

		r = rand() % (40 + 1);

		if (r == 40)
		{
			puts("YOU WON!!! (KEEP GAMBLING FOR MORE RED40)");
			RED40 = getppid();
			break;
		}
		RED40--;

		printf("\nGambling... YOU LOST. You have %d RED40 remaining\n", RED40);
		puts("I'm a winner see my prize, you're a loser who sits and cries");
	}
}

void warn_msg()
{
	char *msg = "You are about to warn the RED40";
	char buf[0x20];
	strncpy(buf, msg, sizeof(buf));
	printf("%s\n", buf);
}

void warn_get()
{
	int c, i = 0;
	char red[0x20];
	memset(red, 0x0, 0x20);

	printf("How will you warn the RED40?\n>\n");
	while ((c = fgetc(stdin)) != '\n' && c != EOF && i < 12)
		red[i++] = c;

	printf(red);

	printf("\nDO YOU HAVE ANYTHING ELSE TO SAY TO THE RED40?????\n> ");

	gets(red);

	if (WARN)
	{
		puts("YOU HAVE BEEN CAUGHT!!! NO MORE WARNING RED40!!!");
		exit(0);
	}
	else
		WARN = 1;
}

void warn()
{
	if (WARN)
	{
		puts("YOU HAVE BEEN CAUGHT!!! NO MORE WARNING RED40!!!");
		exit(0);
	}

	warn_msg();
	warn_get();
}

void consume()
{
	printf("How much RED40 would you like to consume? You have %d RED40\n\n> ", RED40);
	int c = getnum();
	RED40 -= c;
	printf("Eating %d RED40 -> You now have %d RED40\n", c, RED40);
}

void steal()

{
	if (STEAL)
	{
		puts("YOU HAVE BEEN CAUGHT!!! NO MORE STEALING RED40!!!");
		exit(0);
	}
	else
		STEAL = 1;

	int c, fd = 0;
	char b;
	char red[0x20];

	puts("It is time to steal RED40!!");
	puts("Where would you like to steal RED40 from?");
	printf("\n> ");
	fgets(red, sizeof(red), stdin);
	red[strnlen(red, sizeof(red)) - 1] = '\0';

	char *red_r = malloc(0x20);
	strncpy(red_r, red, 0x20);

	int count = 0;
	const char delim[] = "/";
	char *last_token = NULL;
	char *token = strtok(red, delim);

	while (token != NULL)
	{
		if (count > 3)
		{
			puts("YOU ARE STEALING TOO MUCH RED40!!!");
			exit(0);
		}
		last_token = token;
		token = strtok(NULL, delim);

		if (count == 0)
		{
			if (strnlen(last_token, strlen(red)) != 4)
			{
				puts("YOU ARE ONLY ALLOWED TO STEAL RED40!!!");
				exit(0);
			}
		}
		else if (count == 2)
		{
			if (strnlen(last_token, strlen(red)) < 4)
			{
				puts("YOU ARE NOT STEALING ENOUGH RED40!!!");
				exit(0);
			}
		}

		count++;
	}

	printf("Count: %d\n", count);
	if (count != 3)
	{
		puts("YOU DON'T LIKE RED40????");
		exit(0);
	}

	fd = open(red_r, O_RDONLY);
	while (read(fd, &b, 1) == 1)
		putchar(b);
	puts("");
	puts("You have stolen a lot of red40...");
	puts("");
}

void loop()
{
	setupv2();
	while (1)
	{
		print_menu();
		printf("\n> ");

		switch (getnum())
		{
		case 1:
			appreciate();
			break;
		case 2:
			gamble();
			break;
		case 3:
			warn();
			break;
		case 4:
			consume();
			break;
		case 5:
			steal();
			break;
		default:
			exit(0);
		}
	}
}

void check()
{
	int fd = open("/proc/sys/kernel/yama/ptrace_scope", O_RDONLY);
	char v;
	read(fd, &v, 1);
	if (v == '1')
	{
		puts("THE RED40 DOESN'T LIKE YOUR SECURITY");
		exit(0);
	}
}

int main(int argc, char *argv[])
{
	setup();
	check();
	if (argc == 2)
	{
		if (!strncmp(argv[1], "loop", 4))
			loop();
	}
}
