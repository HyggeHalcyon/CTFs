import numpy as np
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

def process_input(input_value):
    num1 = np.array([0], dtype=np.uint64)
    num2 = np.array([0], dtype=np.uint64)
    num2[0] = 0
    print(f'[1] {num1=}, {num2=}')
    a = input_value
    if a < 0:
        return "Exiting..."
    num1[0] = (a + 65)
    print(f'[2] {num1=}, {num2=}')
    print(f'[*] {num2[0] - num1[0]}')
    if (num2[0] - num1[0]) == 1337:
        return 'You won!\n'
    return 'Try again.\n'

if __name__ == '__main__':
    print(f'[!] MIN = {np.iinfo(np.uint64).min}')
    print(f'[!] MAX = {np.iinfo(np.uint64).max}')

    # 64 not 65 to account for the inclusive `0`
    # 18446744073709551615 - (64 + x) = 1337
    input_value = int("18446744073709550214".strip())
    print(process_input(input_value))