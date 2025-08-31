import binascii
import json
import re
import base64
from Crypto.Cipher import AES

# Hard-coded key and IV from enc.js
KEY_HEX = "6c27f0f1a2f0e4b14b3a5b7c9d1e2f3a6c27f0f1a2f0e4b14b3a5b7c9d1e2f3a"
IV_HEX  = "1a2b3c4d5e6f708190a0b0c0d0e0f001"

KEY = bytes.fromhex(KEY_HEX)
IV  = bytes.fromhex(IV_HEX)

def decrypt_value(b64val: str) -> str:
    """
    Decrypt a single encrypted value produced by enc.js.
    The JS encodes: Base64( AES-CTR( Base64(value) ) || IV ).
    """
    raw = base64.b64decode(b64val)
    ct, iv = raw[:-16], raw[-16:]
    cipher = AES.new(KEY, AES.MODE_CTR, nonce=b'', initial_value=iv)
    pt_bytes = cipher.decrypt(ct)
    # Payload itself is a base64 string, decode again
    plain_b64 = pt_bytes.decode()
    return base64.b64decode(plain_b64).decode(errors="replace")

def extract_char_from_payload(sql_payload: str) -> tuple[int, str]:
    """
    Parse SQLi payload: ' OR SUBSTRING(passwordd,N,1)='X' AND SLEEP(5)#
    Return (N, X).
    """
    m = re.search(r"SUBSTRING\(passwordd,(\d+),1\)='(.)'", sql_payload)
    if not m:
        return None, None
    return int(m.group(1)), m.group(2)

def process_hex_payload(hex_str: str):
    """
    Convert hex -> JSON -> decrypt -> extract character.
    """
    try:
        js = binascii.unhexlify(hex_str).decode()
        # print(js)
        data = json.loads(js)
    except Exception as e:
        print("Invalid JSON:", e)
        return None

    dec_user = decrypt_value(data["username"])
    dec_pass = decrypt_value(data["password"])
    pos, char = extract_char_from_payload(dec_pass)

    if pos and char:
        print(f"Position {pos} = {char}")
        return pos, char
    return None

if __name__ == "__main__":
    # Example: replace with your tshark hex lines
    hex_payloads = []
    tmp = []
    with open("out", "r") as f:
        tmp = f.read().split('\n')
    
    for i in range(len(tmp)):
    # for i in range(1):
        if tmp[i] == "":
            continue
        try:
            # print(tmp[i].split("\t")[6])
            hex_payloads.append(tmp[i].split("\t")[6])
            # print(hex_payloads[i])
        except Exception as e:
            print(e)
            print(tmp[i])


    flag_chars = {}
    for hex_str in hex_payloads:
        res = process_hex_payload(hex_str)
        if res:
            pos, char = res
            flag_chars[pos] = char

    # Reconstruct partial flag
    flag = "".join(flag_chars.get(i, "?") for i in range(1, max(flag_chars)+1))
    print("\nRecovered flag so far:", flag)
    print(flag.upper())
