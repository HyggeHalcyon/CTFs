#!/usr/bin/bash

USERNAME='bandit12'
HOST='bandit.labs.overthewire.org'
PASSWORD='JVNBBFSmZwKKOP0XbFXOoW8chDz5yVRv'
PORT=2220

SOLUTION="mkdir /tmp/cok; cp data.txt /tmp/cock; cd /tmp/cock; xxd -r data.txt data.gz; gzip -d data.gz; bzip2 -d data; mv data.out data.gz; gzip -d data.gz; tar -xf data; tar -xf data5.bin; bzip2 -d data6.bin; tar -xf data6.bin.out; mv data8.bin data8.gz; gzip -d data8.gz; cat data8"

sshpass -p ${PASSWORD} ssh -o StrictHostKeyChecking=no ${USERNAME}@${HOST} -p ${PORT} ${SOLUTION}