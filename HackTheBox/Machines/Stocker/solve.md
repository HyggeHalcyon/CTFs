# Solve

1. http static page, so expect no directories.
2. search for subdomains    
    `gobuster vhost -u stocker.htb --append-domain -w /SecLists-master/Discovery/DNS/subdomains-top1million-5000.txt -o vhost.txt`
3. found development page with login, vulnerable to nosql injection
4. purchase and add to basket, creating a vulnerable PDF
5. using iframe and `file://` protocol to inject LFI within PDF
6. read `/var/www/dev/index.js` to retrieve user password
7. `sudo -l` reveals we can run node as root that is vulnerable to Path Traversal
8. run `exploit.js` to spawn shell as root