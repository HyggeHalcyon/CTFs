# Solve

1. nmap scan, reveals filtered http port `80`
2. visit another web open for public at port `55555`
3. outdated with SSRF CVE, use it to make a request to `127.0.0.1:80`
4. reveals the web behind port `80`, another outdated with RCE vulnerability to gain reverse shell
5. `sudo -l` reveals we can run `systemctl` with sudo
6. we can run shell commands within `systemctl` just like inside of `vim`. abuse it to spawn as root 