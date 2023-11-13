seqid = [109, 51, 77, 111, 114, 105, 101, 53, 95, 85, 110, 76, 48, 99, 75, 69, 100] 
flag = []

for i in range(len(seqid)):
    if(isinstance(seqid[i], int)):
        flag.append(chr(seqid[i]))  
    else:
        flag.append(seqid[i])

print(''.join(flag))