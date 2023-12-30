push   rbp
mov    rbp,rsp
push   rbx
sub    rsp,0x28
mov    QWORD PTR [rbp-0x28],rdi
mov    rax,QWORD PTR [rbp-0x28]
mov    rdi,rax
call   0x5555555550e0 <strlen@plt>
cmp    rax,0x20
je     0x5555555558a1
mov    eax,0x0
jmp    0x555555555912
mov    DWORD PTR [rbp-0x14],0x0
jmp    0x555555555907
mov    eax,DWORD PTR [rbp-0x14]
movsxd rdx,eax
mov    rax,QWORD PTR [rbp-0x28]
add    rax,rdx
movzx  eax,BYTE PTR [rax]
mov    BYTE PTR [rbp-0x16],al
mov    BYTE PTR [rbp-0x15],0x0
mov    eax,DWORD PTR [rbp-0x14]
cdqe
lea    rdx,[rax*8+0x0]
lea    rax,[rip+0x282b]        # 0x555555558100
mov    rbx,QWORD PTR [rdx+rax*1]
lea    rax,[rbp-0x16]
mov    rdi,rax
call   0x555555555299
mov    rdi,rax
call   0x5555555553ef
mov    rsi,rbx
mov    rdi,rax
call   0x555555555140 <strcmp@plt>
test   eax,eax
je     0x555555555903
mov    eax,0x0
jmp    0x555555555912
add    DWORD PTR [rbp-0x14],0x1
cmp    DWORD PTR [rbp-0x14],0x1f
jle    0x5555555558aa
mov    eax,0x1
mov    rbx,QWORD PTR [rbp-0x8]
leave
ret
sub    rsp,0x8
add    rsp,0x8
ret