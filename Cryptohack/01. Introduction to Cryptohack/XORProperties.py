key1 = "a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313"

key1_key2 = "37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e"
key2 = hex( (int(key1, 16) ^ int(key1_key2, 16)) )

key2_key3 = "c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"
key3 = hex( (int(key2, 16) ^ int(key2_key3, 16)) )

ciphertext = "04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"
plaintext = hex( (int(ciphertext, 16) ^ int(key1, 16) ^ int(key2, 16) ^ int(key3, 16)) ) 

flag = "".join([chr(i) for i in bytes.fromhex(plaintext[2:])])

print("Flag: " + flag)
