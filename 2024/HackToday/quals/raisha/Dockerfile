FROM ubuntu:23.10 as ubuntu

FROM pwn.red/jail

COPY --from=ubuntu / /srv

COPY flag.txt /srv/app/flag.txt
COPY raisha /srv/app/run