# Solve

1. intercept hhtp request to 10.129.83.214 reveals its dns -> pi.hole
2. confirm with `dig @10.129.83.214 pi.hole`
3. update `/etc/host`
4. pi is a reference to raspbery pi, login through ssh using default creds.txt
5. sudo -i immediately to root
6. root.txt is missing, backup is on usb device
7. run `df -lh` to show disks
8. cd `/media/usbstick` and the files on usb has been deleted
9. run `strings` on the device file `/dev/sdb` and the history shows the root.txt there 