#!/usr/bin/bash

USERNAME='bandit6'
HOST='bandit.labs.overthewire.org'
PASSWORD='P4L4vucdmLnm8I7Vl7jG1ApGSfjYKqJU'
PORT=2220

SOLUTION='cd /; find ./ -user bandit7 -group bandit6 -size 33c -readable 2>dev/null; cat ./var/lib/dpkg/info/bandit7.password'

sshpass -p ${PASSWORD} ssh -o StrictHostKeyChecking=no ${USERNAME}@${HOST} -p ${PORT} ${SOLUTION}