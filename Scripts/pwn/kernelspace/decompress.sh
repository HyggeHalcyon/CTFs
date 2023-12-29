#!/bin/bash

if [ "$1" = "" ]; then
    echo "usage: $0 <initramfs.cpio.gz>";
else

    # Decompress a .cpio.gz packed file system
    mkdir initramfs
    pushd . && pushd initramfs
    cp ../$1 .
    gzip -dc $1 | cpio -idm &>/dev/null && rm $1
    popd
fi