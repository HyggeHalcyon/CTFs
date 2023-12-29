#!usr/bin/python3
from pwn import *
from threading import Thread
from queue import Queue

# =========================================================
#                          SETUP                         
# =========================================================
exe = './chall'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'debug'
host, port = '', 1337

# https://www.pythontutorial.net/python-concurrency/python-threading/
# https://www.pythontutorial.net/python-concurrency/python-stop-thread/
# https://captain-woof.medium.com/picoctf-guessing-game-2-walkthrough-ret2libc-stack-cookies-6f9fc39273bf
# https://realpython.com/intro-to-python-threading/

class fuzzer():
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

# =========================================================
#                         FUZZING
# =========================================================
guess = fuzzer(10).start()