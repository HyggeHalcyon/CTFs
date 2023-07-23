#!/usr/bin/bash

sshpass -p guest ssh -o StrictHostKeyChecking=no col@pwnable.kr -p2222

# to download
# sshpass -p guest scp -P2222 col@pwnable.kr:/home/col/col .
# sshpass -p guest scp -P2222 col@pwnable.kr:/home/col/col.c .