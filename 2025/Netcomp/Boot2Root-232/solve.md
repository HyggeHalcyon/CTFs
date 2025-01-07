1. directory fuzzing using ffuz using [dirsearch](https://github.com/maurosoria/dirsearch)'s wordlist founds `/backup.zip`
2. within `backup.zip` there's an unusual file `jsut in case.txt` which contains the credentials `pasta:oasis123oasis123` to user.txt
3. `ss -lntp` founds uncommon port 98 listening on localhost, use ssh forward tunnel to access it within our machine `sudo ssh -L 98:localhost:98 pasta@10.1.2.232`
4. the port listens for HTTP request which servers a Backdrop CMS. within it there's a post by admin
5. tries to login using admin username using several default password and `admin:admin` works
6. accessing the dashboard the version seems to be vulnerable to a [public exploit](https://www.exploit-db.com/exploits/52021)
7. using the exploit we gain a web shell which runs as `ottosir` which able to run `/usr/bin/su` as sudo NOPASSWD
8. gain interactive shell using reverse shell to su to root and gain root.txt