import string

enc = [22,15,32,11,43,44,24,25,14,24,14,11,31,11,51,24,51,11]

for i in range(1, 27):
    flag = [chr(c % i) for c in enc]
    print(''.join(flag))