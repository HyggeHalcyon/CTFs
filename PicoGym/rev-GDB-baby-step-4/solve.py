import gdb
import re

gdb.execute("file debugger0_d")
instruction = gdb.execute("x/i 0x401114", to_string=True).strip()

# split using regex
instruction = re.split(r',|\t| ', instruction)
print(instruction)

print('picoCTF{' + str(int(instruction[-1][2:], 16)) + '}')