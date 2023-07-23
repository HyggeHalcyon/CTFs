p = 29

for a in range(0, p):
    if(pow(a, 2, p) == 18):
        print(a)

ints = [14, 6, 11]
residue_roots = [[], [], []]

# finding residue roots
for i in range(0, 3):  
    for a in range(0, p):
        if(pow(a, 2, p) == ints[i]):
            residue_roots[i].append(a)

print(f'{residue_roots=}')

# searching for the minimum root on each ints 
for i in range(0, 3):
    if residue_roots[i]:
        for j in residue_roots[i]:
            print(f'Quardratic Residue: {j}')
        print(f'Flag: {min(residue_roots[1])}')