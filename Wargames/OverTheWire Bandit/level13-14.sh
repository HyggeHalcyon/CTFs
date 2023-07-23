#!/usr/bin/bash

USERNAME='bandit13'
HOST='bandit.labs.overthewire.org'
PASSWORD='wbWdlBxEir4CaE8LaPhauuOo6pwRmrDw'
PORT=2220

# sshpass -p ${PASSWORD} scp -P ${PORT} ${USERNAME}@${HOST}:sshkey.private .

# chmod 700 sshkey.private

USERNAME='bandit14'
SOLUTION="cat /etc/bandit_pass/bandit14; nc localhost 30000;"
PASSWORD='fGrHPx402xGC7U7rXKDaxiWFTOiF0ENq'

ssh -i sshkey.private -o StrictHostKeyChecking=no ${USERNAME}@${HOST} -p ${PORT} ${SOLUTION}