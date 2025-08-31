#!/bin/bash
set -e

while true; do
    f=$(ls *.zip* 2>/dev/null | head -n1)
    [ -z "$f" ] && break   # stop if no zip-like files left
    echo "[*] Extracting $f"
    unzip -o "$f" >/dev/null 2>&1 || break
    rm -f "$f"
done

echo "[+] Done. Remaining files:"
ls -l
