#!/bin/sh

docker build -t noname .
docker run -d --name noname -p 1337:1337 noname

