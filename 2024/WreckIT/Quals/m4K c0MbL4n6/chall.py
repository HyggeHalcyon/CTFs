from propietary import *
def print_diagram():
    diagram = """
    Sistem Penjodohan oleh Mak Comblang. Semoga cocok :)
    """

    print(diagram)

if __name__ == "__main__":
    print_diagram()



while True:
	X_hex = input('choose your man (hex): ')
	Y_hex = input('choose your woman (hex): ')
	
	hash_value1 = HORTEX(Y_hex)
	hash_value2 = HORTEX(Y_hex)

	# print(Y_hex == X_hex)
	# print(hash_value1 == hash_value2)
	
	if hash_value1 == hash_value2 and X_hex != Y_hex:
		print("New couple is matched :). Here your flag WRECKIT50{REDACTED}")
		break
	else:
		print("Try again")
		break