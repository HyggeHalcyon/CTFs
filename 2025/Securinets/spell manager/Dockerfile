FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y socat
RUN rm -rf /var/lib/apt/lists/*

RUN useradd -m ctf

COPY ./main /home/ctf/challenge
COPY ./flag.txt /home/ctf/flag.txt

RUN chown -R root:ctf /home/ctf && \
    chmod 750 /home/ctf/challenge && \
    chmod 640 /home/ctf/flag.txt

EXPOSE 9090

CMD ["socat", "TCP-LISTEN:9090,reuseaddr,fork", "EXEC:/home/ctf/challenge,su=ctf,stderr"]
