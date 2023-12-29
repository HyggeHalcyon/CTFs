#!/bin/bash

if [ "$1" = "" ]; then
    echo "usage: $0 <exploit.c>";
else

    # Compress initramfs with the included statically linked exploit
    in=$1
    out=$(echo $in | awk '{ print substr( $0, 1, length($0)-2 ) }')
    musl-gcc $in -static -pie -s -O0 -fPIE -o $out || exit 255
    mv $out initramfs
    pushd . && pushd initramfs
    find . -print0 | cpio --null --format=newc -o 2>/dev/null | gzip -9 > ../initramfs.cpio.gz
    popd
fi