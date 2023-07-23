#!/usr/bin/bash

USERNAME='bandit8'
HOST='bandit.labs.overthewire.org'
PASSWORD='TESKZC0XvTetK0S9xNwm25STk5iWrBvP'
PORT=2220

SOLUTION='cat data.txt | sort | uniq -u'

sshpass -p ${PASSWORD} ssh -o StrictHostKeyChecking=no ${USERNAME}@${HOST} -p ${PORT} ${SOLUTION}