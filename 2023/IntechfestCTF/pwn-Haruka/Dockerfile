FROM ubuntu:latest

RUN useradd -ms /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

USER root

RUN apt-get -y update
RUN apt-get -y install socat lua5.4

RUN mkdir -p /ctf
WORKDIR /ctf
COPY main.lua .

EXPOSE 1337

USER ctf
CMD socat TCP-LISTEN:1337,reuseaddr,fork 'EXEC:lua main.lua'