#!/usr/bin/bash

USERNAME='bandit1'
HOST='bandit.labs.overthewire.org'
PASSWORD='NH2SXQwcBdpmTEzi3bvBHMM9H66vVXjL'
PORT=2220

SOLUTION='cat < -'

sshpass -p ${PASSWORD} ssh -o StrictHostKeyChecking=no ${USERNAME}@${HOST} -p ${PORT} ${SOLUTION}