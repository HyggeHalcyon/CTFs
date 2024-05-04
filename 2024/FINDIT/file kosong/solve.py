# https://ctf.samsongama.com/ctf/forensics/picoctf19-whitepages.html
with open('flag.txt', 'rb') as f:
    content = f.read()
    # print(content)
    s = content.replace(b'\xE2\x80\x83', b'0').replace(b'\x20', b'1').replace(b' ', b'')
    for i in range(0, len(s), 8):
        print(chr(int(s[i:i+8], 2)), end='')

# FindITCTF{Pl3as3_3x!t_th3_pl4tf0rm}