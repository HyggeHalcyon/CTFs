FROM ubuntu:23.10 as ubuntu

FROM pwn.red/jail

COPY --from=ubuntu / /srv

COPY flag.txt /srv/flag.txt
COPY vuln /srv/app/run