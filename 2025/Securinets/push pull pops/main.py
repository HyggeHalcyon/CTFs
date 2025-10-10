#!/usr/local/bin/python3
import mmap
import ctypes
import base64
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_GRP_AVX2
from capstone import CS_OP_REG


def check(code: bytes):
    if len(code) > 0x2000:
        return False

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    for insn in md.disasm(code, 0):
        name = insn.insn_name()
        print(name)
        if name!="pop" and name!="push" :
            if name=="int3" :
                continue
            return False
        if insn.operands[0].type!=CS_OP_REG:
            return False
            
        
    return True

def run(code: bytes):

    # Allocate executable memory using mmap
    
    mem = mmap.mmap(-1, len(code), prot=mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC)
    mem.write(code)
    
    # Create function pointer and execute
    func = ctypes.CFUNCTYPE(ctypes.c_void_p)(ctypes.addressof(ctypes.c_char.from_buffer(mem)))
    func()
    
    exit(1)

def main():
    code = input("Shellcode : ")
    code = base64.b64decode(code.encode())
    try:
        if check(code):
            run(code)
        else:
            raise AssertionError("check failed")
    except Exception as e:
        print("Exception type :", type(e)) 
        print("Exception text :", e)       
        
        exit(1)

if __name__ == "__main__":
    main()