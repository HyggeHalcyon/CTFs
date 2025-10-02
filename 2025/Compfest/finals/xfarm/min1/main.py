#!/usr/bin/env python3


from exploitfarm import *

def get_ip_port(data, key):
    key = str(key)  # ensure string for lookup
    return data.get("data", {}).get(key, [None])[0]

team_id = get_host()
# team_id = '16'
json_data = {'data': {'6': ['10.0.38.14:40001'], '7': ['10.0.38.14:40003'], '8': ['10.0.38.14:40005'], '9': ['10.0.38.14:40007'], '10': ['10.0.38.14:40009'], '11': ['10.0.38.14:40011'], '12': ['10.0.38.14:40013'], '13': ['10.0.38.14:40015'], '14': ['10.0.38.14:40017'], '15': ['10.0.38.14:40019'], '16': ['10.0.38.14:40021'], '17': ['10.0.38.14:40023'], '18': ['10.0.38.14:40025'], '19': ['10.0.38.14:40027'], '20': ['10.0.38.14:40029']}, 'status': 'success'}
host = get_ip_port(json_data, team_id)
if host is None:
    print("[-] No host found for team ID:", team_id)

from pwn import *
from binascii import unhexlify, hexlify
import os
import re

from md5 import *
from rand import *  

def xor(a: bytes, b: bytes) -> bytes:
    max_len = max(len(a), len(b))
    a_padded = a.ljust(max_len, b"\x00")
    b_padded = b.ljust(max_len, b"\x00")
    return bytes(x ^ y for x, y in zip(a_padded, b_padded))

def isNeighbor(u, v, edges):
    return (u, v) in edges or (v, u) in edges

# context.log_level = 'debug'
# io = process(["python3", "min/chall.py"], cwd="..")  
io = remote(host.split(":")[0], int(host.split(":")[1]))
valid_colors = {
    b'red'  : b'\xa0iS\x9c\x04\x1b\xf0\xb9o]\x84N7\x0c\xe8f',
    b'green': b'\x17\xce\x12[\x19\x9f\x00p]-\x8a\x1e\x14\x9c\xf0\xba',
    b'blue' : b'\xb3\xe8n\xc7\xfcf\xf1sF\xc9\x96\x1awPL\xed',
}

# b'red': a069539c041bf0b96f5d844e370ce866
# b'green': 17ce125b199f00705d2d8a1e149cf0ba
# b'blue': b3e86ec7fc66f17346c9961a77504ced

edges = [
    (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
    (2, 3), (2, 4), (2, 5), (2, 6),
    (3, 7), (3, 8), (4, 7), (4, 8),
    (5, 7), (5, 8), (6, 7)
]

print(isNeighbor(1, 2, edges))
coloring = {
    1: b'red',
    2: b'green',
    3: b'blue',
    4: b'blue',
    5: b'blue',
    6: b'blue',
    7: b'red',
    8: b'green',
}

io.sendlineafter(b'> ', b'1')

# stage 1
for i in range(30):
    keys = {}
    commits = {}
    for v in range(1, 9):
        k = b'00' * 16
        keys[v] = k
        H = hash(k)                     
        color_hash = valid_colors[coloring[v]]
        C = xor(color_hash, H)              
        commits[v] = C

    for v in range(1, 9):
        prompt = f'Enter commitment for vertex {v}: '.encode()
        io.sendlineafter(prompt, commits[v].hex().encode())

    io.recvuntil(b'Verifier selected edge: ')
    line = io.recvline().strip()  
    m = re.match(br'\((\d+),\s*(\d+)\)', line)
    if not m:
        io.interactive()
        break

    u = int(m.group(1))
    v = int(m.group(2))

    io.sendlineafter(f'Enter key for vertex {u}: '.encode(), keys[u].hex().encode())
    io.sendlineafter(f'Enter key for vertex {v}: '.encode(), keys[v].hex().encode())

edges=[
    (1, 2), (1, 3), (1, 4), (1, 5), (2, 3),
    (2, 4), (2, 5), (3, 4), (3, 5), (4, 5),
    (1, 6), (2, 6), (3, 6), (4, 6), (5, 6),
    (6, 7)
]

for _ in range(100):
    for v in range(1, 8):
        io.sendlineafter(f'Enter commitment for vertex {v}: '.encode(), b'0' * 32)

    io.recvuntil(b'Verifier selected edge: ')
    m = re.match(br'\((\d+),\s*(\d+)\)', io.recvline().strip()); assert m
    u, v = int(m.group(1)), int(m.group(2))

    io.sendlineafter(f'Enter key for vertex {u}: '.encode(), hexlify(b'red'))
    io.sendlineafter(f'Enter key for vertex {v}: '.encode(), hexlify(b'green'))

io.recvuntil(b"Alright, it seems that you can be trusted. Here's the secret: ")
io.recvline()
flag = io.recvline().strip().decode()
print(flag)

io.close()