#!/usr/bin/bash

USERNAME=''
HOST=''
PASSWORD=''
PORT=1337

SOLUTION='whoami; ls; pwd;'

sshpass -p ${PASSWORD} ssh -o StrictHostKeyChecking=no ${USERNAME}@${HOST} -p ${PORT} ${SOLUTION}