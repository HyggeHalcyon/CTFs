FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get -y install socat gcc make

RUN groupadd -r user && useradd -r -g user user

ADD ./init.sh /etc/init.sh
RUN chmod 700 /etc/init.sh

WORKDIR /home/user/
ADD ./junior_formatter junior_formatter
ADD ./flag.txt flag.txt
RUN chmod 550 junior_formatter

RUN chown -R root:user /home/user

ENTRYPOINT "/etc/init.sh"
