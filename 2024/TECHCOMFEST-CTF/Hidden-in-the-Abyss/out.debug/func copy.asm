push   rbp
mov    rbp,rsp
push   rbx
sub    rsp,0x28
mov    QWORD PTR [INPUT],rdi

mov    rax,QWORD PTR [INPUT]
mov    rdi,rax                               
call   0x5555555550e0 <strlen@plt>
cmp    rax,0x20
je     0x5555555558a1

mov    eax,0x0
jmp    0x555555555912

mov    DWORD PTR [rbp-0x14],0x0        -> 0x10
jmp    0x555555555907

mov    eax,DWORD PTR [rbp-0x14]
movsxd rdx,eax
mov    rax,QWORD PTR [INPUT]
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
call   0x555555555299 -> ret 7fc56270e7a70fa81a5935b72eacbe29 // DIFFERENT

mov    rdi,rax
call   0x5555555553ef -> ret 92ebcae27b5395a18af07a7e07265cf7 // DIFFERENT

mov    rsi,rbx
mov    rdi,rax
call   0x555555555140 <strcmp@plt> -> 3d137ff4afbdf0b6afbfa059c81ece9b 

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