cts = []
p2 = 0

with open("c1", "rb") as f:
    c1 = f.read()
    c1 = [i for i in c1]
    cts.append(c1)

with open("c2", "rb") as f:
    c2 = f.read()
    c2 = [i for i in c2]
    cts.append(c2)

with open("c3", "rb") as f:
    c3 = f.read()
    c3 = [i for i in c3]
    cts.append(c3)

with open("p2", "rb") as f:
    p2 = f.read()
    p2 = [i for i in p2]

k = []
for i in range(0, len(p2)):
    k.append((p2[i] ^ cts[1][i]))

p1 = []
for i in range(0, len(cts[0])):
    p1.append((k[i] ^ cts[0][i]))

p3 = []
for i in range(0, len(cts[2])):
    p3.append((k[i] ^ cts[2][i]))

print(''.join([chr(i) for i in p1]))
print(''.join([chr(i) for i in p3]))