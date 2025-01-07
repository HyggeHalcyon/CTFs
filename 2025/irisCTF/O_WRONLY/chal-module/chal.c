// SPDX-License-Identifier: GPL-2.0-or-later
/*
 * This kernel module has serious security issues (and probably some implementation
 * issues), and might crash your kernel at any time. Please don't load this on any
 * system that you actually care about. I recommend using a virtual machine for this.
 * You have been warned.
 */

#include <linux/fs.h>
#include <linux/namei.h>
#include <linux/uio.h>
#include <linux/module.h>
#include <linux/version.h>
#include <linux/syscalls.h>
#include <linux/kprobes.h>
#include <linux/kernel.h>
#include <linux/unistd.h>
#include <linux/fdtable.h>
#include <asm/paravirt.h>

#define TARGET_FILE_CONTENT "Permission Denied\n"
#define TARGET_FILE_NAME "vda"

static ssize_t phony_read(struct file * f, char __user * buf, size_t size, loff_t * off) {
	const char* target = TARGET_FILE_CONTENT;
	const size_t target_size = sizeof(TARGET_FILE_CONTENT);

	loff_t curr = *off;

	if (curr >= target_size)
		return 0;

	if (copy_to_user(buf, target + curr, target_size - curr) != 0)
		return -EFAULT;

	*off += target_size - curr;

	return target_size - curr;
}

static ssize_t phony_write(struct file * f, const char __user * buf, size_t size, loff_t * off) {
	*off += size;
	return size;
}


static struct file_operations phony_operations = {
	.read = phony_read,
	.write = phony_write,
	.llseek	= generic_file_llseek,
};

struct file_input {
	int flags;
	char name[2000];
};

static struct file* get_cursed(int flags) {
	struct file* cursed = filp_open("/dev/null", flags, 0);
	cursed->f_op = &phony_operations;
	return cursed;
}

static int open_entry_handler(struct kretprobe_instance *ri, struct pt_regs *regs) {
	struct file_input* input = (struct file_input*)ri->data;

	input->flags = ((struct open_how *)regs->dx)->flags;

	int len = strncpy_from_user(input->name, (char __user*)regs->si, 2000);
	if (unlikely(len <= 0)) {
		return 1;
	}

	int i;
	for (i = len; i > 0 && input->name[i] != '/'; i--);

	if (input->name[i] == '/')
		i++;

	if (i >= 2000)
		i = 0;

	if (strcmp(input->name + i, TARGET_FILE_NAME) == 0) {
		return 0;
	}

	return 1;
}

static int open_handler(struct kretprobe_instance *ri, struct pt_regs *regs) {
	struct file_input* input = (struct file_input*)ri->data;

	unsigned long fd;
    if (!is_syscall_success(regs)) {
		fd = get_unused_fd_flags(input->flags);
		regs_set_return_value(regs, fd);
    }
	

	if (is_syscall_success(regs)) {
		fd = regs_return_value(regs);

		struct fdtable *fdt;
		rcu_read_lock_sched();
		smp_rmb();
		fdt = rcu_dereference_sched(current->files->fdt);
		struct file* f = get_cursed(input->flags);
		rcu_assign_pointer(fdt->fd[fd], f);
		rcu_read_unlock_sched();
	}

	return 0;
}

struct kretprobe syscall_kprobe_open = {
	.handler = open_handler,
	.entry_handler = open_entry_handler,
	.data_size = sizeof(struct file_input),
	.maxactive = 20
};


static int ph_read_init(void) {
	syscall_kprobe_open.kp.symbol_name = "do_sys_openat2";
	register_kretprobe(&syscall_kprobe_open);

	return 0;
}

static void ph_read_exit(void) {
	unregister_kretprobe(&syscall_kprobe_open);
}

module_init(ph_read_init);
module_exit(ph_read_exit);

MODULE_DESCRIPTION("I'm sorry...");
MODULE_AUTHOR("LambdaXCF <hello@lambdaxcf.com>");
MODULE_LICENSE("GPL");

