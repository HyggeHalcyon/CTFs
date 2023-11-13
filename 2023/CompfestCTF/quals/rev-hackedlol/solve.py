cs = open("source.py").read()
file=open("important_file.hackedlol", "rb").read()
f = open("flag.txt", "wb")

for h in range(len(file)):
    f.write(chr(file[h] ^ ord( cs[(h * 39) % len(cs)] )).encode())