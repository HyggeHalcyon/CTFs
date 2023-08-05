# Solve

1. scan nmap, visit searcher.htb, based on the version is vulnerable to RCE 
2. gain reverse shell using a public exploit
3. need password for `sudo -l`, available on `.git` config file at the web directory `(var/www/app)` which gives us a password `cody` and a username `jh1usoih2bkjaspwe92` which we can also use for `sudo -l` (though the machine name is svc and not cody)
4. `sudo -l` we can run `system-checkup.py` that has some functionalities on the deployed docker
5. `sudo /usr/bin/python3 /opt/scripts/system-checkup.py full-checkup` reveals a subdomain `gitea.searcher.htb`
6. visiting `gitea.searcher.htb` we can login as cody which then we also found that there's a administrator account
7. `sudo /usr/bin/python3 /opt/scripts/system-checkup.py docker-inspect  --format='{{json .}}' <container>` gives us the container configuration which reveals the root/administrator mysql password
8. use the leaked password to login as administator at `gitea.searcher.htb`
9. take a look at the scripts source code
10. `full-checkup` is ran without absolute path, we can abuse this
11. cd to `/tmp` directory
12. create `full-checkup.sh` with reverse shell command and set up a listener
13. run `sudo /usr/bin/python3 /opt/scripts/system-checkup.py full-checkup` inside `/tmp`
14. we shall gain shell and pwned