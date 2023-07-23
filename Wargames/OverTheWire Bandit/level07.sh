#!/usr/bin/bash

USERNAME='bandit7'
HOST='bandit.labs.overthewire.org'
PASSWORD='z7WtoNQU2XfjmMtWA8u5rN4vzqu4v99S'
PORT=2220

SOLUTION='cat data.txt | grep -n millionth'

sshpass -p ${PASSWORD} ssh -o StrictHostKeyChecking=no ${USERNAME}@${HOST} -p ${PORT} ${SOLUTION}