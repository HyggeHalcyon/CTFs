FROM ubuntu:latest

RUN apt-get -y update --fix-missing
RUN apt-get -y upgrade
RUN apt-get -y update --fix-missing

FROM pwn.red/jail
COPY --from=0 / /srv
RUN mkdir /srv/app
COPY ./ctf /srv/app/run
COPY ./flag.txt /srv/app/

RUN chmod 555 /srv/app/run
RUN chmod 444 /srv/app/flag.txt

WORKDIR /srv/app
RUN mv flag.txt flag-$(md5sum flag.txt | awk '{print $1}').txt

ENV JAIL_MEM=20M JAIL_TIME=300 JAIL_PORT=33337
EXPOSE 33337
