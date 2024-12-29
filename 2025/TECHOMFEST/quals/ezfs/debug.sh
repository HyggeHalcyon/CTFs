#!/bin/bash

./exp/compress.sh ./exp/exploit.c
qemu-system-x86_64 \
	-m 64M \
        -cpu qemu64,+smep,+smap \
        -nographic \
        -monitor none \
        -kernel bzImage \
        -initrd debugfs.cpio.gz \
	-no-reboot \
	-drive file=flag.txt,format=raw \
	-append "console=ttyS0 quiet kaslr panic=1 kpti=1 oops=panic" \
	-net user -net nic -device e1000
