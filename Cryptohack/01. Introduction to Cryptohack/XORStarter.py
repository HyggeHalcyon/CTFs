initial_string = "label"
decimal_representation = [ord(i) for i in initial_string]
xored_representation = [i^13 for i in decimal_representation]
encrypted_ascii = [chr(i) for i in xored_representation]
flag = "crypto{" + "".join(encrypted_ascii) + "}"


print("Flag: " + flag)