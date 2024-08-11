#!/bin/bash
# run this as normal user
clear
timeout --foreground 28000 /usr/bin/qemu-system-x86_64 \
	-m 256M \
	-kernel ./bzImage \
	-initrd ./debugfs.cpio.gz \
	-fsdev local,security_model=passthrough,id=fsdev0,path=/tmp/fak\
	-device virtio-9p-pci,id=fs0,fsdev=fsdev0,mount_tag=hostshare\
	-nographic \
	-monitor none \
	-no-reboot \
	-append "console=ttyS0 nokaslr nosmap nosmep nokpti quiet panic=0" \
	-s
