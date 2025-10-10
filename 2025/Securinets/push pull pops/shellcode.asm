    BITS 64
    DEFAULT REL

    section .text
    global _start

_start:
    xor rdx, rdx                 ; envp = NULL
    mov rbx, 0x0068732f6e69622f  ; "/bin/sh\0" in little-endian (mov rbx, 0x0068732f6e69622f)
    push rbx
    mov rdi, rsp                 ; rdi -> "/bin/sh"
    push rdx                     ; push 0 (NULL terminator for argv)
    push rdi                     ; push pointer to "/bin/sh"
    mov rsi, rsp                 ; rsi -> ["/bin/sh", NULL]
    mov eax, 59                  ; syscall execve
    syscall
