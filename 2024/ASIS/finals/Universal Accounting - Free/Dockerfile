FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt -y update --fix-missing && apt-get -y upgrade
RUN apt -y install xinetd
RUN groupadd -r pwn && useradd -r -g pwn pwn

ADD pwn.xinetd /etc/xinetd.d/pwn
ADD init.sh    /etc/init.sh
ADD redir.sh   /home/pwn/redir.sh
RUN chmod 700 /etc/init.sh
RUN chmod 1733 /tmp /var/tmp /dev/shm

WORKDIR /home/pwn
ADD flag.txt  flag.txt
ADD chall chall
RUN chmod 440 flag.txt
RUN chmod 550 chall
RUN chmod 550 redir.sh
RUN mv flag.txt flag-$(md5sum flag.txt | awk '{print $1}').txt

RUN chown -R root:pwn /home/pwn

RUN ls -al /home/pwn

RUN service xinetd restart

EXPOSE 9999
CMD ["/etc/init.sh"]