#!/usr/bin/python3
from hidden import *

while True:
    ans = input(
        "\nExplore and discover the profound essence of this journey, as you seek out the genuine truth that lies within\n$ "
    ).strip()

    if any(char in ans for char in block):
        print("ILLEGAL")
        # print(
        #     f"\n{ascii1}\nYour journey is blocked by something; perhaps this is not the time for the truth to appear.\n-FIND IT 2024\n"
        # )
    else:
        try:
            tmp = ans + "()"
            print("[!] INPUT:", tmp)
            eval(tmp)
            print("Is this the true ending???\n")
        except sussy:
            print("SUSSY")
            # print(f"\n{ascii2}\nOh no! Maybe you forgor something.\nAmogus!!\n")
        except anothersussy:
            print("ANOTHER SUSSY")
            # print(
            #     f"\n{ascii2}\nOh no! Maybe take a step back to see the whole journey again.\nAmogus!!\n"
            # )
        except:
            print("IDK")
            # print(f"\n{ascii2}\nOh no! Maybe this is not the correct path.\nAmogus!!\n")

# solve:
# https://github.com/b01lers/b01lers-ctf-2023-public/blob/main/misc/blacklisted/solve.md
# https://github.com/salvatore-abello/pyjail/blob/main/B01lers%20CTF%202023/Blacklisted.py 
# get redacted part of the source code:
# print(getattr(open('hidden.p''y','r'),'read')())
# Explore and discover the profound essence of this journey, as you seek out the genuine truth that lies within
# $ print(getattr(open('rilll/flag.txt',mode='ra'.replace('a',chr((ord('z')^ord('B')^ord('Z'))))),'read')())
# b'FindITCTF{4m0GU5_y0u_Sh0u1d_ch3ck_4ll_th3_f1l3s}'