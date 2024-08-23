from pwn import *

context.log_level = 'debug'

def factorial(number) -> int:
    if number == 0:
        return 1
    return number * factorial(number - 1)

if __name__ == '__main__':
    host, port = "206.189.32.77", 9901
    io = remote(host, port)

    round = 0
    while (round < 1000):
        io.recvuntil(b'dari ')
        io.recvuntil(b'dari ')
        number = io.recvuntil(b'?', drop=True)
        ans = factorial(int(number))

        log.info(f'Round[{round}] Number: {number} Factorial: {ans}')
        io.sendline(str(ans))
        round = round + 1

    io.interactive()
