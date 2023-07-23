#!/usr/bin/bash

sshpass -p guest ssh -o StrictHostKeyChecking=no random@pwnable.kr -p2222

# to download
# sshpass -p guest scp -P2222 random@pwnable.kr:/home/random/random .
# sshpass -p guest scp -P2222 random@pwnable.kr:/home/random/random.c .