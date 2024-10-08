#define VERSION     "69.420"
#define DESCRIPTION "Touching some digital grass"
#define AUTHOR      "NeoZap"
#define LICENSE     "GPL"

#define DEVICE_NAME "camping"
#define KINTRO 0xCABE0000
#define KGREET 0xCABE0001
#define KVISIT 0xCABE0002
#define BUFFER_SIZE 0x100

#include <linux/module.h>
#include <linux/printk.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/ctype.h>
#include <linux/delay.h>
#include <linux/mutex.h>

static int major;
static DEFINE_MUTEX(camping_mutex);

struct visitor_data {
    char name[BUFFER_SIZE];
    uint64_t location;
    char decoration[BUFFER_SIZE];
} visitor;

static long camping_intro(unsigned long arg) {
    if (copy_from_user(&visitor, (struct visitor_data __user *)arg, sizeof(visitor))) {
        printk(KERN_ALERT "camping: intro failed\n");
        return -EFAULT;
    }
    printk(KERN_INFO "camping: Welcome! Let's go camping and relax~\n");
    return 0;
}

static long camping_greet(unsigned long arg) {
    char hello[] = KERN_ALERT "camping: Hello, ";
    char greeting[BUFFER_SIZE + sizeof(hello) + 1];

    memcpy(greeting, hello, sizeof(hello));
    memcpy(greeting + sizeof(hello) - 1, visitor.name, BUFFER_SIZE);

    printk(greeting);
    printk(KERN_INFO "camping: I see you're ready for an adventure, let's visit a nice campsite! :)\n");
    return 0;
}

static long camping_visit(unsigned long arg) {
    printk(KERN_INFO "camping: So you want to visit that campsite huh, okay here we go!\n");

    if (!access_ok((void __user *)visitor.location, BUFFER_SIZE)) {
        printk(KERN_ALERT "camping: Sorry, that campsite is not open yet! ~_~\n");
        return -EFAULT;
    }

    printk(KERN_INFO "camping: It looks a bit plain... let's add some decorations!\n");

    int len = strnlen(visitor.decoration, BUFFER_SIZE);
    for (int i = 0; i < len; i++) {
        if (!isalnum(visitor.decoration[i])) {
            printk(KERN_ALERT "camping: That decoration is... a bit questionable?\n");
            return -EINVAL;
        }
    }

    printk(KERN_INFO "camping: Decorating...\n");
    memcpy((void __user *)visitor.location, visitor.decoration, len + 1);

    printk(KERN_INFO "camping: Done! Your campsite is now beautifully decorated :)\n");
    printk(KERN_INFO "camping: Enjoy your camping experience!\n");
    return 0;
}

static long camping_ioctl(struct file *file, unsigned int cmd, unsigned long arg) {
    switch (cmd) {
        case KINTRO:
            return camping_intro(arg);
        case KGREET:
            return camping_greet(arg);
        case KVISIT:
            return camping_visit(arg);
        default:
            printk(KERN_ALERT "camping: Invalid command\n");
            return -EINVAL;
    }
}

static int camping_open(struct inode *inode, struct file *file) {
    if (!mutex_trylock(&camping_mutex)) {
        printk(KERN_ALERT "camping: Device is busy!\n");
        return -EBUSY;
    }
    printk(KERN_INFO "camping: Device opened\n");
    return 0;
}

static int camping_release(struct inode *inode, struct file *file) {
    mutex_unlock(&camping_mutex);
    printk(KERN_INFO "camping: Device closed\n");
    return 0;
}

static struct file_operations fops = {
    .unlocked_ioctl = camping_ioctl,
    .open = camping_open,
    .release = camping_release,
};

int init_module(void) {
    printk(KERN_INFO "camping: Initializing...\n");

    major = register_chrdev(0, DEVICE_NAME, &fops);
    if (major < 0) {
        printk(KERN_ALERT "camping: Failed to register a major number %d\n", major);
        return major;
    }
    printk(KERN_INFO "camping: Registered correctly with major number %d\n", major);
    return 0;
}

void cleanup_module(void) {
    unregister_chrdev(major, DEVICE_NAME);
    printk(KERN_INFO "camping: Plays \"Mimosa - Eri Sasaki\"🎵🎶\n");
}

MODULE_AUTHOR(AUTHOR);
MODULE_DESCRIPTION(DESCRIPTION);
MODULE_LICENSE(LICENSE);
MODULE_VERSION(VERSION);
