#!/bin/bash

./exp/compress.sh ./exp/exploit.c
qemu-system-x86_64 \
    -m 128M \
    -kernel bzImage \
    -initrd debugfs.cpio.gz \
    -append "console=ttyS0 loglevel=3 oops=panic panic=1 pti=off kaslr quiet" \
    -cpu qemu64,+smep \
    -monitor /dev/null \
    -nographic \
    -no-reboot -s