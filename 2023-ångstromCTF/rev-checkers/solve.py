#!user/bin/python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
exe = './checkers'
io = process(exe)
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'


# =========================================================
#                         EXPLOITS
# =========================================================

# String compare found in ghidra
string = "actf{ive_be3n_checkm4ted_21d1b2cebabf983f}"

io.sendline(string)

io.interactive()