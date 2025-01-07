#ifndef CHECKSUMZ_API_H
#define CHECKSUMZ_API_H

/* You may want to include this from userspace code, since this describes the valid ioctls */

#include <sys/types.h>
#ifdef __KERNEL__
#include <linux/types.h>
#include <linux/ioctl.h>
#else /* !__KERNEL__ */
#include <stddef.h>
#include <sys/ioctl.h>
#include <stdint.h>
#define __user /* __user means nothing in userspace, since everything is a user pointer anyways */
#endif

struct checksum_buffer {
	loff_t pos;
	char state[512];
	size_t size;
	size_t read;
	char* name;
	uint32_t digest;
};

#define CHECKSUMZ_IOCTL_RENAME   _IOWR('@', 0, char*)
#define CHECKSUMZ_IOCTL_PROCESS  _IO('@', 1)
#define CHECKSUMZ_IOCTL_RESIZE   _IOWR('@', 2, uint32_t)
#define CHECKSUMZ_IOCTL_DIGEST   _IOWR('@', 3, uint32_t*)

#endif /* SONGBIRD_API_H */

