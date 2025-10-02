./exp/compress.sh ./exp/exploit.c || exit 255

qemu-system-x86_64 \
    -kernel "./artifacts/bzImage" \
    -initrd "./debugfs.cpio.gz" \
    -append "oops=panic panic=1 console=ttyS0 nofgkaslr nokaslr quiet" \
    -nographic \
    -serial stdio \
    -monitor none \
    -nic user,model=virtio-net-pci \
    -no-reboot \
    -snapshot \
    -m 64M \
    -cpu max,+smap,+smep,enforce \
    -drive id=flag,file="./flag.txt",format=raw,if=virtio \
    -s