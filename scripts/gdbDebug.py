import gdb

gdb.execute("file <chall>")
gdb.execute("break *<func>+offset")
gdb.execute("run")
memory = gdb.execute("x/4xb $rbp-0x4", to_string=True)

# return value
rax = gdb.selected_frame().read_register("rax")
print(rax)