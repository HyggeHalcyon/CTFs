from capstone import Cs, CS_ARCH_X86, CS_MODE_64
code = b"\x50\x58\x50\x58" + b"\xc4" + b"\x90\x90\x90"  # prefix of push/pop, then a lone 0xC4, then payload
code = b'\xCC\x09\x01\x0F\xF0'
md = Cs(CS_ARCH_X86, CS_MODE_64)
decoded = 0
for i in md.disasm(code, 0):
    print(i.mnemonic, i.op_str, i.size)
    decoded += i.size
print("len(code)=", len(code), "decoded=", decoded)
