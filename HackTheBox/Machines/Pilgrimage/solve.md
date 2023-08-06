# Solve

1. nmap scan shows `.git` directory is found. use `git-dumper` to extract it
2. the server is using a vulnerable `ImageMagick` to `CVE-2022-44268`
3. recreate the public PoC using `./run-cve.sh`
    - `./run-cve.sh craft <path>` to craft payload to be uploaded
    - save the shrunken image and run `./run-cve result` to show the result in hex
4. analysing the source code, we have a SQLite database `var/db/pilgrimage` which contains emily's password
5. running linpeas we discover the following result  
`╔══════════╣ .sh files in path`  
`/usr/bin/gettext.sh`                               
`/usr/sbin/malwarescan.sh`  
**malwarescan.sh** in particular is interesting because we have read permissions, and the script is running binwalk in a outdated version  
6. utilizing `inotifywait`, binwalk will execute if a file is created within `var/www/pilgrimage.htb/shrunk/`
7. the binwalk version is vulnerable to `CVE-2022-4510`. Using public PoC we recreate is as follows:
    - set up a netcat listener
    - cd into `var/www/pilgrimage.htb/shrunk/`
    - setup the PoC script and a png file
    - run the script 
    - pwned