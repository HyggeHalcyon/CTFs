#!/bin/sh

./exp/compress.sh ./exp/exploit.c || exit 255

qemu-system-x86_64 \
    -initrd debugfs.cpio.gz \
    -kernel bzImage \
    -append 'console=ttyS0 root=/dev/ram nokaslr oops=panic panic=1' \
    -monitor /dev/null \
    -m 64M \
    --nographic  \
    -smp cores=1,threads=1 \
    -s \
    -cpu kvm64,+smep 