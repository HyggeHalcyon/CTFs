FROM ubuntu:24.04 as ubuntu

FROM pwn.red/jail

COPY --from=ubuntu / /srv

COPY flag.txt /srv/app/flag.txt

COPY chall /srv/app/run