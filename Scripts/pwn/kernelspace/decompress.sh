#!/bin/bash

if [ "$1" = "" ]; then
    echo "usage: $0 <fs.cpio.gz>";
else

    # Decompress a .cpio.gz packed file system
    mkdir debugfs
    pushd . && pushd debugfs
    cp ../$1 .
    gzip -dc $1 | cpio -idm &>/dev/null && rm $1
    popd
fi