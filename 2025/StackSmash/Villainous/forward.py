#!/usr/bin/env python3
from pwn import *
import threading

context.log_level = 'info'

LISTEN_HOST = '127.0.0.1'
LISTEN_PORT = 1337
FORWARD_HOST = '127.0.0.1'
FORWARD_PORT = 7331

def forward(src, dst):
    try:
        while True:
            data = src.recv(4096)
            if not data:
                break
            dst.send(data)
            if src is client:
                log.info(f"[{src.sock.getsockname()}] -> [{dst.sock.getsockname()}]: {data!r}")
    except EOFError:
        pass
    except Exception as e:
        log.error(f'Forwarding error: {e}')

def main():
    global io
    global client

    log.info(f'Listening on {LISTEN_HOST}:{LISTEN_PORT} and forwarding to {FORWARD_HOST}:{FORWARD_PORT}')

    server = listen(LISTEN_PORT, bindaddr=LISTEN_HOST)
    client = server.wait_for_connection()
    log.success(f'Got connection from {client.sock.getpeername()}')
    
    try:
        io = remote(FORWARD_HOST, FORWARD_PORT)
        log.success(f'Connected to forward target {FORWARD_HOST}:{FORWARD_PORT}')
    except Exception as e:
        log.error(f'Failed to connect to forward target: {e}')
        client.close()
        return

    t1 = threading.Thread(target=forward, args=(client, io))
    t2 = threading.Thread(target=forward, args=(io, client))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    client.close()
    io.close()

if __name__ == '__main__':
    main()
