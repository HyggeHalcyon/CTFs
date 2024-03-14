from pwn import *
import struct

TEMP_EXE_FILE = 'temp'
context.log_level = 'info'
host, port = '94.237.63.2', 51470

def get_key() -> str:
    elf = ELF(TEMP_EXE_FILE, checksec=True)
    
    opcode = elf.read(elf.entry + 7, 0x4)
    offset = struct.unpack('<i', opcode)[0]
    addr = (elf.entry + 4) + offset + 0x7
    key = elf.read(addr, 24).hex()

    info('entry: %#x', elf.entry)
    info('opcode:: %#s', opcode)
    info('offset: %#x', offset) 
    info('addr: %#x', addr)

    return key

def handle():
    io = remote(host, port)

    for i in range(1, 130):
        info("COUNTER = %d", i)

        io.recvuntil(b'ELF:  ')
        encoded = io.recvline()
        temp = open(TEMP_EXE_FILE, 'wb')
        temp.write(base64.b64decode(encoded))
        temp.close()

        key = get_key()
        io.sendlineafter(b'Bytes?', key.encode())
    
    io.interactive()

if __name__ == '__main__':
    handle()