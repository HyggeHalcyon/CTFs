import base64, hmac, hashlib
from Crypto.Cipher import AES

shared_hex = "9f4c8b2e6a7f1d3b9ab2c4d5e6f70812a1b2c3d4e5f60718293a4b5c6d7e8f90"
secret = bytes.fromhex(shared_hex)
aes_key = secret[:16]
hmac_key = secret[16:]

def decrypt_message(b64msg):
    blob = base64.b64decode(b64msg)
    iv = blob[:16]
    ct = blob[16:-32]
    tag = blob[-32:]

    calc = hmac.new(hmac_key, iv + ct, hashlib.sha256).digest()
    if calc != tag:
        raise ValueError("HMAC failed")

    aes = AES.new(aes_key, AES.MODE_CBC, iv)
    padded = aes.decrypt(ct)
    padlen = padded[-1]
    return padded[:-padlen].decode("utf-8", errors="ignore")

with open("extracted_b64.txt") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            print("Decrypted:", decrypt_message(line))
        except Exception as e:
            print("Failed:", e)
