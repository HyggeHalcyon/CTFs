#include <linux/kernel.h>
#include <linux/syscalls.h>
#include <linux/kmod.h>
#include <asm/uaccess_64.h>

SYSCALL_DEFINE2(naup, void __user *, kaddr, const char __user *, str) {
    char buf[8];

    if ((char *)kaddr != modprobe_path) {
        printk(KERN_INFO "naup syscall: Invalid address!\n");
        return -EPERM;
    }

    if (copy_from_user(buf, str, 8)) {
        printk(KERN_INFO "naup syscall: copy_from_user failed!\n");
        return -EFAULT;
    }

    memcpy(kaddr, buf, 8); 

    printk(KERN_INFO "naup syscall: copied 8 bytes to modprobe_path (%p)\n", kaddr);

    return 0;
}

