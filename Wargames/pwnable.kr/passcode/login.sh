#!/usr/bin/bash

sshpass -p guest ssh -o StrictHostKeyChecking=no passcode@pwnable.kr -p2222

# to download
# sshpass -p guest scp -P2222 passcode@pwnable.kr:/home/passcode/passcode .
# sshpass -p guest scp -P2222 passcode@pwnable.kr:/home/passcode/passcode.c .