from subprocess import run

run("nasm -f bin shellcode.asm -o shellcode.bin", shell=True, check=True)

with open("shellcode.bin", "rb") as f:
    print("var shellcode = [")
    while chunk := f.read(8):
        hex_value = chunk.hex()
        little_endian_hex = ''.join([hex_value[i:i+2] for i in range(0, len(hex_value), 2)][::-1])
        print(f'\t0x{little_endian_hex}n,')
    print("];")