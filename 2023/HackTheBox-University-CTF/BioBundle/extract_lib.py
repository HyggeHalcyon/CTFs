from pwn import *

FLAG = []
PREFIX = b'pwndbg'

context.log_level = 'info'
def main():
    io = process(['gdb-pwndbg', '-q', 'biobundle'])
    io.recvlines(4)

    # extracted shared object
    file = open("out.lib", "wb+")

    for i in range(15879):
        # read each byte of __
        io.sendlineafter(PREFIX, f'x/b (long)&__+{i}'.encode())
        io.recvuntil(b'>:\t')

        # get each byte of __
        result = int(io.recvline().strip()) ^ 55
        print(result, i)
        
        # write result to file
        file.write(result.to_bytes(1, 'little', signed=True)) 

    io.close()

if __name__ == '__main__':
    main()