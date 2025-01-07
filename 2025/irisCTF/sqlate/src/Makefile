OBJS	= main.o sqlite.o base64.o
SOURCE	= main.c sqlite.c base64.c
HEADER	= main.h sqlite.h base64.h
OUT	= vuln
FLAGS	= -masm=intel -g -c -Wall
LFLAGS	=
CC	= gcc

all: vuln

vuln: $(OBJS)
	$(CC) -g $(OBJS) -o $(OUT) $(LFLAGS)

main.o: main.c
	$(CC) $(FLAGS) main.c

base64.o: base64.c
	$(CC) $(FLAGS) base64.c

sqlite.o: sqlite.c
	$(CC) $(FLAGS) sqlite.c

clean:
	rm -f $(OBJS) $(OUT)