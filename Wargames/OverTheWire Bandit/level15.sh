#!/usr/bin/bash

USERNAME='bandit15'
HOST='bandit.labs.overthewire.org'
PASSWORD='jN2kgmIXJ6fShzhT2avhotn4Zcka6tnt'
PORT=2220
SOLUTION=''

ssh -i sshkey.private -o StrictHostKeyChecking=no ${USERNAME}@${HOST} -p ${PORT} #${SOLUTION}