#!/bin/bash

chall_specific_parameters="nofgkaslr"

kernel="$(realpath ./artifacts/bzImage)"
initramfs="$(realpath ./artifacts/debugfs.cpio.gz)"
flag="$(realpath ./flag)"

cmdline="oops=panic panic=1 console=ttyS0 $chall_specific_parameters"
qemu_args=()
debug=1

while [ "$#" -gt 0 ]; do
    case "$1" in
        --debug)           debug=1;;
        --kernel=*)        kernel="${1#--kernel=}";;
        --initramfs=*)     initramfs="${1#--initramfs=}";;
        --flag=*)          flag="${1#--flag=}";;
        --append=*)        cmdline="${cmdline} ${1#--append=}";;
        --root)            cmdline="${cmdline} init.stay-root";;
        --)                shift; qemu_args+=("$@"); break;;
        *)                 echo "Unknown argument: $1"; exit 1;;
    esac
    shift
done

if [ "${debug}" -eq 1 ]; then
    # Enable debugger
    qemu_args+=(-s)

    # Disable kaslr
    cmdline="${cmdline} nokaslr"
else
    cmdline="${cmdline} quiet"
fi

./artifacts/exp/compress.sh ./artifacts/exp/exploit.c
qemu-system-x86_64 \
    -kernel "$kernel" \
    -initrd "$initramfs" \
    -append "$cmdline" \
    -nographic -serial stdio -monitor none -nic user,model=virtio-net-pci \
    -no-reboot -snapshot \
    -m 512M \
    -cpu max,+smap,+smep,enforce \
    -drive id=flag,file="./flag",format=raw,if=virtio \
    "${qemu_args[@]}"


setterm -linewrap on
