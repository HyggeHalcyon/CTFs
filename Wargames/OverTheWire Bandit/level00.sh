#!/usr/bin/bash

USERNAME='bandit0'
HOST='bandit.labs.overthewire.org'
PASSWORD='bandit0'
PORT=2220

SOLUTION='cat readme'

sshpass -p ${PASSWORD} ssh -o StrictHostKeyChecking=no ${USERNAME}@${HOST} -p ${PORT} ${SOLUTION}