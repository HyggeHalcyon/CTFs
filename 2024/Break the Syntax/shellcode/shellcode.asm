    BITS 64
    DEFAULT REL

    section .text
    global _start

_start:
    ; pread64(0x3, rsp, 0x40, 0x0)
    mov rdi, 0x3
    mov rsi, rsp
    mov rdx, 0x40
    mov r10, 0x0
    mov rax, 17
    syscall

    ; write(0x1, rsp, 0x40)
    mov rdi, 0x1
    mov rsi, rsp
    mov rdx, 0x40
    mov rax, 0x1
    syscall

    nop
    nop
    nop

flagpath: db "this is not being used", 0