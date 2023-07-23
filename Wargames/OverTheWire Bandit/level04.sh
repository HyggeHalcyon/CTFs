#!/usr/bin/bash

USERNAME='bandit4'
HOST='bandit.labs.overthewire.org'
PASSWORD='2EW7BBsr6aMMoJ2HjW067dm8EgX26xNe'
PORT=2220

SOLUTION='cd inhere/; cat < -file07'

sshpass -p ${PASSWORD} ssh -o StrictHostKeyChecking=no ${USERNAME}@${HOST} -p ${PORT} ${SOLUTION}