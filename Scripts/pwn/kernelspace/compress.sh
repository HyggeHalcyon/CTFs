#!/bin/bash

if [ "$1" = "" ]; then
    echo "usage: $0 <exploit.c>";
else

    # Compress file system with the included statically linked exploit
    in=$1
    out=$(echo $in | awk '{ print substr( $0, 1, length($0)-2 ) }')
    musl-gcc $in -static -lpthread -pie -s -O0 -fPIE -o $out || exit 255
    cp $out debugfs
    pushd . && pushd debugfs
    find . -print0 | cpio --null --format=newc -o 2>/dev/null | gzip -9 > ../debugfs.cpio.gz
    popd
fi