#!user/bin/python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
io = remote('challs.actf.co', 32760)
exe = './zaza'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'


# =========================================================
#                         EXPLOITS
# =========================================================

# Got through RE on ghidra
string = "2& =$!-( <*+*( ?!&$$6,. )' $19 , #9=!1 <*=6 <6;66#"
key = "anextremelycomplicatedkeythatisdefinitelyuselessss"

# basic comparison pass
io.sendlineafter(b'Count me some sheep: ', b'4919')
io.sendlineafter(b': ', b'12')

# convert to iterable ordinal form
string_ordinal = [ord(i) for i in string]
key_ordinal = [ord(i) for i in key]

# magic word will be xor with key to match with string
# basic xor properties to get magic word
magic_word = ""
for i in range(0, len(string)):
    magic_word += chr(string_ordinal[i] ^ key_ordinal[i])

# show magic word
info("magic word: %s", magic_word)

# send last comparison
io.sendlineafter(b'magic word?', magic_word)

io.interactive()