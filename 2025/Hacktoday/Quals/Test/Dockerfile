FROM ubuntu:25.04 AS ubuntu

FROM pwn.red/jail

COPY --from=ubuntu / /srv

COPY flag.txt /srv/app/flag.txt
COPY a.out /srv/app/run