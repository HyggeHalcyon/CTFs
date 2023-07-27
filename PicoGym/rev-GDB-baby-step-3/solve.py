import gdb

gdb.execute("file debugger0_c")
gdb.execute("break *main+15")
gdb.execute("run")
gdb.execute("n")
memory = gdb.execute("x/4xb $rbp-0x4", to_string=True)

memory = memory.strip().split("\t")
flag = []
for i in range(1, 5):
    flag.append(memory[i][2:])

print('PicoCTF{0x' + ''.join(flag) + '}')