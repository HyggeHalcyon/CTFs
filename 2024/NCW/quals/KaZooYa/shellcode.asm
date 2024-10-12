    BITS 64
    DEFAULT REL

    section .text
    global _start

_start:
    lea rdi, [sh]
    xor rsi, rsi
    xor rdx, rdx
    mov rax, 0x3b
    syscall

sh: db "/bin/sh", 0