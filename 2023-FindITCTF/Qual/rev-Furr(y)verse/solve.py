key = '@ch^CN=N@um*f+^Y/*F+^Y/If+>w' 
flag = []

for i in key: 
    flag.append(chr(ord(i) + 0x6))
    
print(''.join([i for i in flag]))