FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get install -y xinetd

RUN useradd -m user

COPY ./chall /home/user/
COPY ./flag.txt /home/user/
COPY run.sh /
COPY xinetd /etc/xinetd.d/user

WORKDIR /home/user

RUN chown -R root:root . && \
    chmod o+rx . && \
    chmod 444 flag.txt && \
    chmod a+x chall && \
    chmod +x /run.sh

RUN apt-get install -y gdb

EXPOSE 1337

CMD ["/usr/sbin/xinetd", "-dontfork"]