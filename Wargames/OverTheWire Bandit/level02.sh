#!/usr/bin/bash

USERNAME='bandit2'
HOST='bandit.labs.overthewire.org'
PASSWORD='rRGizSaX8Mk1RTb1CNQoXTcYZWU6lgzi'
PORT=2220

SOLUTION='cat spaces\ in\ this\ filename; cat "spaces in this filename"'

sshpass -p ${PASSWORD} ssh -o StrictHostKeyChecking=no ${USERNAME}@${HOST} -p ${PORT} ${SOLUTION}