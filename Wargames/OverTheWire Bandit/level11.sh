#!/usr/bin/bash

USERNAME='bandit11'
HOST='bandit.labs.overthewire.org'
PASSWORD='6zPeziLdR2RKNdNYFNb6nVCKzphlXHBM'
PORT=2220

SOLUTION='strings data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m''

sshpass -p ${PASSWORD} ssh -o StrictHostKeyChecking=no ${USERNAME}@${HOST} -p ${PORT} ${SOLUTION}