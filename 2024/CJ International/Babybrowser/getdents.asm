    BITS 64
    DEFAULT REL

    section .text
    global _start
    
_start:
    ; fd = sys_open(".", 0, 0)
    lea rdi, [dirname]
    xor rsi, rsi
    xor rdx, rdx
    mov rax, 0x2
    syscall

    mov rdi, rax  ; fd

    ; getdents(fd,esp,0x1337)
    mov rsi, rsp
    mov rdx, 0x1337 ;size
    mov rax, 78
    syscall

    ; sys_write
    mov rdi, 0x1
    mov rax, 0x1
    syscall

dirname:
    db '.', 0x0