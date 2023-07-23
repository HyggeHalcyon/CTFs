#!/usr/bin/bash

USERNAME='bandit5'
HOST='bandit.labs.overthewire.org'
PASSWORD='lrIWWI6bB37kxfiCQZqUdOIYfr6eEeqR'
PORT=2220

SOLUTION='cd inhere/; find -readable -size 1033c; cat ./maybehere07/.file2'

sshpass -p ${PASSWORD} ssh -o StrictHostKeyChecking=no ${USERNAME}@${HOST} -p ${PORT} ${SOLUTION}