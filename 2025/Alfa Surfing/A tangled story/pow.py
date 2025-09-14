#!/usr/bin/env python3
import hashlib, selectors, socket, sys, time, os, random, string

BITS = 21  # fixed by the binary

def md5_ok(b: bytes) -> bool:
    # Fast integer check for "leading zero bits"
    h = int.from_bytes(hashlib.md5(b).digest(), "big")
    return (h >> (128 - BITS)) == 0

def find_one(prefix_len: int = 12) -> bytes:
    """
    Precompute ONE printable line whose MD5 has 21 leading zero bits.
    Uses a random prefix to avoid reuse collisions on the server.
    Returns the exact bytes to send (no newline).
    """
    alphabet = string.ascii_lowercase + string.digits
    prefix = "g-" + "".join(random.choice(alphabet) for _ in range(prefix_len)) + "-"
    n = 0
    pref_b = prefix.encode()
    while True:
        cand = pref_b + str(n).encode()
        if md5_ok(cand):
            return cand
        n += 1

def relay_interactive(sock: socket.socket):
    sock.setblocking(False)
    sel = selectors.DefaultSelector()
    sel.register(sock, selectors.EVENT_READ)
    sel.register(sys.stdin, selectors.EVENT_READ)
    try:
        while True:
            for key, _ in sel.select():
                if key.fileobj is sock:
                    try:
                        data = sock.recv(4096)
                    except BlockingIOError:
                        continue
                    if not data:
                        print("\n[+] Connection closed by remote.")
                        return
                    sys.stdout.write(data.decode(errors="replace"))
                    sys.stdout.flush()
                else:
                    line = sys.stdin.readline()
                    if not line:
                        return
                    sock.sendall(line.encode())
    finally:
        sel.unregister(sock)
        sel.unregister(sys.stdin)

def main():
    # if len(sys.argv) != 3:
    #     print(f"Usage: {sys.argv[0]} HOST PORT", file=sys.stderr)
    #     sys.exit(1)
    host, port = "46.62.167.155", 31337

    # 1) PRECOMPUTE the line (this may take a little while, but happens BEFORE connecting)
    t0 = time.time()
    line = find_one()
    md5hex = hashlib.md5(line).hexdigest()
    print(f"[+] Precomputed line: {line!r}")
    print(f"[+] MD5: {md5hex}  (meets {BITS} leading zero bits)")
    print(f"[+] Precompute time: {time.time() - t0:.2f}s")

    # 2) CONNECT and send it immediately (server gives only ~3s to reply)
    with socket.create_connection((host, port), timeout=10.0) as s:
        # Read banner quickly (non-blocking ok; banner is short)
        try:
            s.settimeout(1.0)
            banner = s.recv(4096)
            if banner:
                sys.stdout.write(banner.decode(errors="replace"))
                sys.stdout.flush()
        except socket.timeout:
            pass

        # Send precomputed solution followed by newline
        s.settimeout(3.0)
        s.sendall(line + b"\n")

        # Read server response (should be "PoW OK. Welcome!\n" on success)
        try:
            resp = s.recv(4096)
            if resp:
                sys.stdout.write(resp.decode(errors="replace"))
                sys.stdout.flush()
        except socket.timeout:
            pass

        print("[+] Entering interactive mode. Ctrl+C to quit.")
        # 3) Interactive relay (stdin <-> socket)
        relay_interactive(s)

if __name__ == "__main__":
    main()