def mangle(val, key):
    return val ^ (key << 7 | key >> 0x39) ^ key

def demangle_ptr(val, key):
    return val ^ (key << 7 | key >> 0x39) ^ key
    
key = 0xee97b5d2e7b89a9d    
asd1 = demangle_ptr(0xa54d5ca13bf5d46a, key)
asd2 = demangle_ptr(0xa54d097a1547d6ca, key)
print("DEMANGLED WITH PTR \t\t" + hex(asd1))
print("DEMANGLED NO PTR \t\t" + hex(asd2))

print("KEY \t\t\t" + hex(0x0 ^ 0xa54d5ca13bf5d46a))
print("KEY VALIDATE \t\t" + hex((key << 7 | key >> 0x39) ^ key))

test = 0x55db2eb202a0 ^ 0xa54d5ca13bf5d46a
print(hex(test))
print(test == 0xa54d097a1547d6ca)

0xa54d5ca13bf5d46a