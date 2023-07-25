#!/usr/bin/bash

sshpass -p guest ssh -o StrictHostKeyChecking=no input2@pwnable.kr -p2222

# to download
# sshpass -p guest scp -P2222 input2@pwnable.kr:/home/input2/input .
# sshpass -p guest scp -P2222 input2@pwnable.kr:/home/input2/input.c .