from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import os
import random
import signal
import base64

FLAG = open("../flag.txt").read()

arr = [] # <- PATCH

class GiftShop:
    def __init__(self, name: str) -> None:
        # snippet...

    def generate_voucher(self) -> str:
        message = self.prefix + os.urandom(93) + self.null + self.Hm
        voucher = pow(int.from_bytes(message, "big"), self.key.d, self.key.n)
        # PATCH BELOW
        arr.append(base64.b64encode(int.to_bytes(voucher, 128, "big")).decode())
        return base64.b64encode(int.to_bytes(voucher, 128, "big")).decode()

    def validate_voucher(self, voucher: str) -> bool:
        if voucher not in arr: # <- PATCH
            return False
        voucher = int.from_bytes(base64.b64decode(voucher.encode()), "big")
        message = int.to_bytes(pow(voucher, self.key.e, self.key.n), 128, "big")
        return (
            # snippet...
        )

class Challenge:
    def __init__(self, name):
        # snippet...

    def greet(self):
        # snippet...

    def __get_bread(self):
        # snippet...

    def __get_voucher(self):
        # snippet...

    def __get_flag(self):
        # snippet...

    def check_available(self):
        # snippet...

    def buy_item(self, item):
        # snippet...

    def redeem_voucher(self, voucher):
        # snippet...

    def admin_code(self, code):
        # snippet...

def user_input(s):
    # snippet...

def main():
    # snippet...

if __name__ == "__main__":
    # signal.alarm(60)
    main()