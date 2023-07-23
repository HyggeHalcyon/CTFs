import base64

ciphertext = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"
decryptedhex = bytes.fromhex(ciphertext)
decryptedbase64 = [i for i in base64.b64encode(decryptedhex)]
flag = ''.join([chr(b) for b in decryptedbase64])

print("Flag: " + flag)