FLAG = "TCF2024{"
ENC_KEY = bytes.fromhex('750e27555971155a')

for i in range(7):
    print(chr(ENC_KEY[i] ^ ord(FLAG[i])), end="") # !MagiC!
print()

ENC_FLAG = bytes.fromhex('750e27555971155a') \
    + bytes.fromhex('0a13540837') \
    + bytes.fromhex('7e7239') \
    + bytes.fromhex('55151d724f') \
    + bytes.fromhex('46123157582d555c') 
KEY = '!MagiC!'

for i in range(len(ENC_FLAG)):
    print(chr(ENC_FLAG[i] ^ ord(KEY[i % len(KEY)])), end="") # TCF2024{Gr3at_St4rt1ng_P01nt}
