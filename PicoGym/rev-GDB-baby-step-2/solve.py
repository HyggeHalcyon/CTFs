import gdb

gdb.execute("file debugger0_b")
gdb.execute("break *main+60")
gdb.execute("run")
eax = gdb.selected_frame().read_register("rax")
print('picoCTF{' + str(eax) + '}')