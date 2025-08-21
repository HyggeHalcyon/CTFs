FROM --platform=linux/amd64 ubuntu:24.04 as builder

RUN apt-get update && \
    apt-get install -y gcc

WORKDIR /app

COPY ./src/baby-heap.c .
RUN gcc baby-heap.c -o baby-heap
RUN rm baby-heap.c

FROM pwn.red/jail

COPY --from=builder / /srv
COPY --from=builder /app/baby-heap /srv/app/run

COPY flag.txt /srv/app

ENV JAIL_TIME=60
