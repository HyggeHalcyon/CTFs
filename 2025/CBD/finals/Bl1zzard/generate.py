import random, string

MAGIC_PRIME = 0x1F2F3F4F
VALIDATION_KEY = 0x41424344
TIME_SEED = 1640995200

def djb2_hash(s: str) -> int:
    h = 5381
    for c in s:
        h = ((h << 5) + h) + ord(c)
    return h & 0xFFFFFFFF

def fnv1a_hash(s: str) -> int:
    h = 2166136261
    for c in s:
        h ^= ord(c)
        h = (h * 16777619) & 0xFFFFFFFF
    return h

def combined_hash(s: str) -> int:
    djb2 = djb2_hash(s)
    fnv1a = fnv1a_hash(s)
    combined = (djb2 ^ fnv1a) & 0xFFFFFFFF
    combined = ((combined << 13) | (combined >> 19)) & 0xFFFFFFFF
    return combined ^ MAGIC_PRIME

def calculate_checksum(s: str) -> int:
    checksum = 0
    for i, c in enumerate(s):
        checksum += ord(c) * (i + 1) * 17
    return (checksum ^ (checksum >> 8) ^ (checksum >> 16)) & 0xFF

def validate_username_format(username: str) -> bool:
    if not (6 <= len(username) <= 10):
        return False
    letters = sum(ch.isalpha() for ch in username)
    digits = sum(ch.isdigit() for ch in username)
    if letters < 2 or digits < 1:
        return False
    ascii_sum = sum(ord(c) for c in username)
    if not (400 <= ascii_sum <= 800):
        return False
    h = combined_hash(username)
    if h % 42 != 0:
        return False
    if (h & 0xFF) != 0x7E:
        return False
    return True

def generate_expected_password(username: str) -> int:
    base_hash = combined_hash(username)
    checksum = calculate_checksum(username)
    transformed = base_hash ^ (checksum * 0x01010101)
    transformed ^= TIME_SEED
    transformed = (transformed * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
    transformed ^= VALIDATION_KEY
    return (transformed % 999999) + 100000

def digit_sum_ok(pw: int) -> bool:
    return sum(int(d) for d in str(pw)) % 7 == 0

def not_palindrome(pw: int) -> bool:
    s = str(pw)
    return s != s[::-1]

# search
while True:
    candidate = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(6,10)))
    if validate_username_format(candidate):
        pw = generate_expected_password(candidate)
        if digit_sum_ok(pw) and not_palindrome(pw):
            print("Found valid pair:", candidate, pw)
            break
