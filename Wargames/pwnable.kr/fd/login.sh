#!/usr/bin/bash

sshpass -p guest ssh -o StrictHostKeyChecking=no fd@pwnable.kr -p2222

# to download
# sshpass -p guest scp -P2222 fd@pwnable.kr:/home/fd/fd .
# sshpass -p guest scp -P2222 fd@pwnable.kr:/home/fd/fd.c .