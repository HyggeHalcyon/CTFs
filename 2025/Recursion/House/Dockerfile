FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y socat

RUN useradd -m recursionctf

WORKDIR /home/recursionctf

COPY ./src/chall /home/recursionctf/chall
COPY ./src/flag.txt /flag.txt

RUN chown -R recursionctf:recursionctf /home/recursionctf
RUN chmod -R 550 /home/recursionctf 

USER recursionctf

EXPOSE 1337

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:/home/recursionctf/chall,stderr"]
