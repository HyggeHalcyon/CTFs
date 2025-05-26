FROM ubuntu:25.04@sha256:008b026f11c0b5653d564d0c9877a116770f06dfbdb36ca75c46fd593d863cbc AS chroot

RUN apt-get update && \
    apt-get --assume-yes --no-install-recommends install socat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./app /app
WORKDIR /app

RUN chmod +x chall.elf
CMD sh start.sh