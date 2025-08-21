# Nmap 7.94SVN scan initiated Fri Aug 15 07:33:21 2025 as: /usr/lib/nmap/nmap --privileged -sC -sV -vv -oA nmap/uree 10.1.2.226
Nmap scan report for 10.1.2.226
Host is up, received reset ttl 63 (0.18s latency).
Scanned at 2025-08-15 07:33:21 EDT for 12s
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE REASON         VERSION
21/tcp open  ftp     syn-ack ttl 63 vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| drwxr-xr-x    2 0        0            4096 Jul 30 21:46 pub
|_drwxr-xr-x    2 0        0            4096 Jul 31 09:03 repo
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.18.0.116
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 4
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 9.2p1 Debian 2+deb12u6 (protocol 2.0)
| ssh-hostkey: 
|   256 18:11:53:ad:32:8d:47:71:70:58:2c:fa:a4:b3:2d:4e (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBFDsNhVP0DPdg4mG+FWHegXf7hXR5qY3CJqgklHojRT6ab7Ad01YD1xHV92qnOvDtx3j4U44dMjxkpzB2e1TmOY=
|   256 9f:1c:1a:0b:96:37:1d:80:7d:37:0e:4b:19:62:12:c7 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBCZ8ItvdUKAFPaACqkrMXMr79q/IWnpIeqkUFLV90bk
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Aug 15 07:33:33 2025 -- 1 IP address (1 host up) scanned in 12.09 seconds
