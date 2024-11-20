#!/bin/bash

./exploit/compress.sh ./exploit/exploit.c

/usr/bin/qemu-system-x86_64 \
	-kernel ./bzImage \
	-initrd ./debugfs.cpio.gz \
	-nographic \
	-monitor none \
	-cpu kvm64,+smap,+smep\
	-append "console=ttyS0 nokaslr kpti panic=0 quiet" \
	-s

