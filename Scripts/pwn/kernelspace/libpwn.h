// inspired by the goat: https://github.com/n132/libx/blob/main/libx.c
#define _GNU_SOURCE
#ifndef LIBPWN_H
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sched.h>
#include <sys/mman.h>
#include <signal.h>
#include <sys/syscall.h>
#include <sys/ioctl.h>
#include <sys/wait.h>
#include <poll.h>
#include <unistd.h>
#include <pthread.h>
#include <string.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <stdint.h>
#include <errno.h>
#include <stddef.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <assert.h>
#include <sys/timerfd.h>
#include <sys/resource.h>
#include <sys/ptrace.h>
#include <sys/user.h>
#include <netinet/tcp.h>  // for SOL_TCP, TCP options
#include <sys/prctl.h>
#include <poll.h>
#include <sys/shm.h>

#define TTYMAGIC                    0x5401
#define PIPE_NUM                    256
#define SOCKET_NUM                  0x20
#define NO_ASLR_BASE                0xffffffff81000000
#define MSG_COPY                    040000

#define TTY_FILE                        "/dev/ptmx"  
#define DEFAULT_FAKE_MODPROBE_PATH      "/tmp/fake"
#define DEFAULT_DEVIOUS_MODPROBE_PATH   "/tmp/pwned"

typedef unsigned long u64;
typedef unsigned int u32;
typedef unsigned short u16;
typedef unsigned char u8;

u64 kbase;
long _proc_cs, _proc_ss, _proc_rsp, _proc_rflags;

typedef struct {
    long mytpe;
    char mtext[1];
} msg_msg_buf;

#endif /* LIBPWN_H */