from string import ascii_letters, digits
from itertools import product
from pwn import log
import eth_utils
import time
import json
import os

def keccak256(password: str, amount: int):
    length = len(password).to_bytes(3, 'big')
    amount = amount.to_bytes(2, 'big')
    return eth_utils.keccak(length + password.encode() + amount)

def commutativeCombine(a, b):
    a = keccak256(a, 0x1000)
    b = keccak256(b, 0x1000)
    if a < b:
        return (a + b).rjust(64, b'\x00')
    return (b + a).rjust(64, b'\x00')

def check_prefix(_a: int) -> bool:
    global founds
    prefix = b'\x00\x00\x3b'

    a = keccak256(_a, 0x1000)
    if a.startswith(prefix):
        founds["prefix"].append(_a)
        cache_file.write(json.dumps(founds))
        log.success(f"Found prefix: {_a}: {a.hex()}")
        return True
    return False

def check_suffix(_a: int) -> bool:
    global founds, cache_file

    a = keccak256(_a, 0x1000)
    if a.endswith(b'\xff\xff'):
        founds["suffix_ffff"].append(_a)
        cache_file.seek(0)
        cache_file.write(json.dumps(founds, indent=4))
        log.success(f"Found suffix: {_a}: {a.hex()}")
        return True
    if a.endswith(b'\x00\x04'):
        founds["suffix_0004"].append(_a)
        cache_file.seek(0)
        cache_file.write(json.dumps(founds, indent=4))
        log.success(f"Found suffix: {_a}: {a.hex()}")
        return True
    return False

def check_commutative(_a: int, _b: int) -> bool:
    global founds

    c = commutativeCombine(_a, _b)

    if c.startswith(b'\x00\x00\x3b'):
        if c.endswith(b'\xff\xff'):
            founds["commutative_ffff"].append({
                "a": _a,
                "b": _b,
            })
        elif c.endswith(b'\x00\x04'):
            founds["commutative_0004"].append({
                "a": _a,
                "b": _b,
            })
        else:
            log.failure(f"Invalid commutative: {_a}:{_b} {c.hex()}")
            return

        cache_file.seek(0)
        cache_file.write(json.dumps(founds, indent=4))
        log.success(f"Found {_a}:{_b} {c.hex()}")

def already_used(_a: str) -> bool:
    global founds
    for f in founds["commutative_ffff"]:
        if f["a"] == _a or f["b"] == _a:
            return True
    for f in founds["commutative_0004"]:
        if f["a"] == _a or f["b"] == _a:
            return True
    return False

def done() -> bool:
    global founds
    if len(founds["commutative_0004"]) >= 1 and len(founds["commutative_ffff"]) >= 4:
        return True
    return False

def main():
    global founds

    max_len = 10

    CHARS = ascii_letters + digits
    for l in range(1, max_len + 1):
        for p in product(CHARS, repeat=l):
            p = ''.join(p)
            if p in founds["prefix"] or p in founds["suffix_ffff"] or p in founds["suffix_0004"]:
                continue

            if check_prefix(p):
                for i in founds["suffix_ffff"]:
                    if len(founds["commutative_ffff"]) >= 4:
                        break
                    if not already_used(i) and not already_used(p):
                        check_commutative(p, i)
                for i in founds["suffix_0004"]:
                    if len(founds["commutative_0004"]) >= 1:
                        break
                    if not already_used(i) and not already_used(p):
                        check_commutative(p, i)
                
            if check_suffix(p):
                for i in founds["prefix"]:
                    if not already_used(i) and not already_used(p):
                        check_commutative(p, i)
                            
            if done():
                break
        if done():
            break

    for f in founds["commutative_ffff"]:
        print(f'ffff -> {f["a"]}:{f["b"]}')
    for f in founds["commutative_0004"]:
        print(f'0004 -> {f["a"]}:{f["b"]}')

if __name__ == "__main__":
    global founds, cache_file

    founds = {
        "prefix": [],
        "suffix_ffff": [],
        "suffix_0004": [],
        "commutative_ffff": [],
        "commutative_0004": []
    }

    if os.path.exists("cache.json"):
        founds = json.load(open("cache.json", "r"))
        cache_file = open("cache.json", "w")
        cache_file.write(json.dumps(founds, indent=4))
    else: 
        cache_file = open("cache.json", "w")

    start = time.time()
    main()
    end = time.time()
    print(f"Time taken: {end - start:.2f} seconds")

