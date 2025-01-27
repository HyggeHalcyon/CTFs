flag = ["x"] * 21

flag[0] = 'a'
flag[2] = 'a'
flag[4] = 'a'
flag[7] = 'a'
flag[9] = 'a'

flag[19] = 'm'
flag[15] = 'p'
flag[10] = 'c'

# ========================

flag[5] = 'p'
flag[1] = 'm'
flag[-1] = 'a'
flag[-1-2] = 'a'
flag[-1-4] = 'a'
flag[-1-7] = 'a'
flag[-1-9] = 'a'

flag[3] = 'n'
flag[-1-3] = 'n'

flag[6] = 'l'
flag[-1-6] = 'l'

flag[8] = 'n'
flag[-1-8] = 'n'

print(flag)
print(''.join(flag))