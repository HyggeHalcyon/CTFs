#!/usr/bin/bash

USERNAME='bandit3'
HOST='bandit.labs.overthewire.org'
PASSWORD='aBZ0W5EmUfAf7kHTQeOwd8bauFJ2lAiG'
PORT=2220

SOLUTION='cd inhere/; ls -a; cat .hidden'

sshpass -p ${PASSWORD} ssh -o StrictHostKeyChecking=no ${USERNAME}@${HOST} -p ${PORT} ${SOLUTION}