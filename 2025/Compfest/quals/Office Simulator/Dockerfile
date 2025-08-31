FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get install -y xinetd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

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

EXPOSE 1338

CMD ["/usr/sbin/xinetd", "-dontfork"]