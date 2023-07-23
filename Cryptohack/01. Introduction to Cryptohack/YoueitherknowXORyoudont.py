#Deciphering Repeated-key XOR Ciphertext

ciphertext = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
knownplaintext = "crypto{"

#convert to Decimal
plainordinal = [ ord(i) for i in knownplaintext ]
cipherordinal = [ i for i in bytes.fromhex(ciphertext) ]

#XOR to cipher with known plain text to find Key
possible_key = ""
for i in range(len(knownplaintext)):
    possible_key += chr(cipherordinal[i] ^ plainordinal[i])  

print(possible_key) #outputs "myXORke" most likely resembling "myXORkey"

#key
key = "myXORkey"
keyordinal = [ ord(i) for i in key ]

#deciphering
flag = ""
for i in range(0, len(cipherordinal)):
    flag += chr(cipherordinal[i] ^ keyordinal[i % len(key)])

print("Flag: " + flag)
