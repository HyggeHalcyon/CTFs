import string

ct = [16, 9, 3, 15, 3, 20, 6, 20, 8, 5, 14, 21, 13, 2, 5, 18, 19, 13, 1, 19, 15, 14]

alpha = string.ascii_uppercase
flag = ''.join([alpha[i-1] for i in ct])

print(f'flag = {flag[:7]}' + '{' + f'{flag[7:]}' + '}')
# PICOCTF{THENUMBERSMASON}