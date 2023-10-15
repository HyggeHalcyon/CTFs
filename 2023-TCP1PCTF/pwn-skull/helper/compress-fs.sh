#!/bin/bash

cd rootfs
mv ../../exploit/exploit .

find . -print0 \
| cpio --null -ov --format=newc \
| gzip -9 > ../rootfs.cpio.gz
