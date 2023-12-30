import hashlib
import string

MD5s = [
    "3d137ff4afbdf0b6afbfa059c81ece9b",
    "7521e341d48b08f214d1dac0738f16d0",
    "21017490f1e4e968f513520349816008",
    "c26841cc98f760f636f2c4d9d827e18c",
    "ad46789f9ffd7e66fe565d594802dcfc",
    "c26841cc98f760f636f2c4d9d827e18c",
    "c2212457b76a1819d17e3f2a976ff78a",
    "605446531ca5a2370658803cdf07b59f",
    "aaec1d22915a22823a4c3f7bc703c9d8",
    "ad46789f9ffd7e66fe565d594802dcfc",
    "e94656b6137dd01f26085f984afe853e",
    "23006ec47629c459550c9d9508b7a41b",
    "e64574a1d280db82707a389ccd89cbd5",
    "ad46789f9ffd7e66fe565d594802dcfc",
    "23006ec47629c459550c9d9508b7a41b",
    "69171c9442ce2032a1a52868f05f9d1c",
    "b94857f6a905ccd028329b0a8324ac4c",
    "da190e616797844b591057d0190e7728",
    "da190e616797844b591057d0190e7728",
    "3fab7a2f9df80382ef2ec5b4e78cbcce",
    "1a36313b7ed15ba14e0acb4da569b8b7",
    "23006ec47629c459550c9d9508b7a41b",
    "92ebcae27b5395a18af07a7e07265cf7",
    "7ecc92917e9c4556cc19f457ddc41af8",
    "e94656b6137dd01f26085f984afe853e",
    "3fab7a2f9df80382ef2ec5b4e78cbcce",
    "132cd3b981019b59dc42653eea0b34b4",
    "23006ec47629c459550c9d9508b7a41b",
    "c2212457b76a1819d17e3f2a976ff78a",
    "33b3102b6558811a7b7629a1e8e59bd2",
    "33b3102b6558811a7b7629a1e8e59bd2",
    "fc5940aadeacd5e9079c50e8dd481bbc"
]

KNOWN = 'TCF2024{' 
FLAG = [None] * 0x20

def solve():
    
    for i in range(len(MD5s)):    
        for char in string.printable + '\n':
            hash = hashlib.md5(char.encode()).digest().hex()[::-1]
            print(f"[!] Comparing {char}:{hash} => {MD5s[i]}")
            if  hash == MD5s[i]:
                FLAG[i] = (char)
                break
        else:
            print(f"[!] Not found => {MD5s[i]}")

if __name__ == '__main__':
    solve()
    print(f"[+] FLAG => {''.join(FLAG)}") # TCF2024{N0t_S0_H1dd3n_Aft3r_4ll}