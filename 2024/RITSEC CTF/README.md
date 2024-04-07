# RITSEC CTF 2024

| Challenge | solved | Category | Description | 
| --- | :---: | :---: | --- |
| Gadget Database | ❌ | pwn | AARCH64 ARM Static binary BOF |
| RIsky Clue | ✅ | pwn | RISC-V ret2win |

RIsky Clue reference:
- https://github.com/datajerk/ctf-write-ups/tree/master/nahamconctf2022/riscky
- https://github.com/nobodyisnobody/write-ups/tree/main/nullcon.HackIM.2022/pwn/typical.ROP

Gadget Database (ARM ROP) study reference:
- https://azeria-labs.com/return-oriented-programming-arm32/
- https://community.arm.com/arm-community-blogs/b/architectures-and-processors-blog/posts/using-the-stack-in-aarch64-implementing-push-and-pop
- https://blog.perfect.blue/ROPing-on-Aarch64
- https://highaltitudehacks.com/2020/09/05/arm64-reversing-and-exploitation-part-1-arm-instruction-set-heap-overflow.html

Was on the last bit of the exploit development. I was already able to control x0, x1, x2 and x8 among others. However somehow the syscall wasn't able or failed to execute(?)

according to the [chromium syscall table](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#arm-32_bit_EABI), the syscall number is at register x8 which is why my exploit is how it is, but it doesn't work. However, according to this [blog](https://highaltitudehacks.com/2020/09/05/arm64-reversing-and-exploitation-part-1-arm-instruction-set-heap-overflow.html) the syscall number is at register x16. At that point the CTF was already over and I'm too tired in reading ARM's assembly.

nonetheless I still learn a lot tho!