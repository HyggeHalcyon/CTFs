FROM ubuntu@sha256:72297848456d5d37d1262630108ab308d3e9ec7ed1c3286a32fe09856619a782 AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY chall /srv/app/run
COPY JOKES FUN_FACTS flag.txt /srv/app
EXPOSE 5000

ENV JAIL_TIME=0
