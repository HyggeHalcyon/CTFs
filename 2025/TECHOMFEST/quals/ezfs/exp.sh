#!/bin/sh

# flag is at /dev/sda
# /dev # dd if=/dev/sda bs=1 count=8 skip=0
# TCF2025{8+0 records in
# 8+0 records out

mknod /tmp/mydevice b 8 0
cat /tmp/mydevice