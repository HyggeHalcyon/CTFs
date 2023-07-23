#!/usr/bin/bash

USERNAME='bandit10'
HOST='bandit.labs.overthewire.org'
PASSWORD='G7w8LIi6J3kTb8A7j9LgrywtEUlyyp6s'
PORT=2220

SOLUTION='strings data.txt | base64 -d'

sshpass -p ${PASSWORD} ssh -o StrictHostKeyChecking=no ${USERNAME}@${HOST} -p ${PORT} ${SOLUTION}