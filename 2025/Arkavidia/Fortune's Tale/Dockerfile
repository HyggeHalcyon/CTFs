FROM alpine

RUN apk add --no-cache \
    fortune \
    socat

RUN addgroup -S ctf && adduser -S ctf -G ctf

COPY flag.txt /home/ctf/flag.txt
COPY chall /home/ctf/chall

RUN chmod 644 /home/ctf/flag.txt \
    && chmod 755 /home/ctf/chall \
    && chown -R root:ctf /home/ctf

WORKDIR /home/ctf
USER ctf
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:./chall,stderr"]
