import gdb

gdb.execute("file debugger0_a")
gdb.execute("break *main+21")
gdb.execute("run")
eax = gdb.selected_frame().read_register("rax")
print('picoCTF{' + str(eax) + '}')