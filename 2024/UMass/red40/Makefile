CFLAGS=-fno-stack-protector -lseccomp

release:
	gcc main.c -o red40 $(CFLAGS)
	gcc parent.c -o parent
	patchelf --set-interpreter ./libc/ld-linux-x86-64.so.2 ./red40
	patchelf --set-rpath ./libc ./red40
