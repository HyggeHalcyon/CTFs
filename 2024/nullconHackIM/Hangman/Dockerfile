FROM debian:latest

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get -y install socat gcc make

RUN groupadd -r user && useradd -r -g user user

ADD ./init.sh /etc/init.sh
RUN chmod 700 /etc/init.sh

WORKDIR /home/user/
ADD ./hangman hangman
ADD ./flag.txt flag.txt
RUN chmod 550 hangman

RUN chown -R root:user /home/user

ENTRYPOINT "/etc/init.sh"
