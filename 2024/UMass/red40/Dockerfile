FROM debian:12-slim as builder

RUN apt update && apt install -y build-essential libseccomp-dev patchelf

WORKDIR /opt/red40
COPY ./main.c /opt/red40/
COPY ./parent.c /opt/red40/
COPY ./Makefile /opt/red40/
COPY ./entrypoint.sh /opt/red40/

RUN make

FROM debian:12-slim as chroot

COPY ./libc /opt/red40/libc
COPY --from=builder /opt/red40/entrypoint.sh /opt/red40
COPY --from=builder /opt/red40/red40 /opt/red40
COPY --from=builder /opt/red40/parent /opt/red40

RUN chmod +x /opt/red40/entrypoint.sh

RUN /usr/sbin/useradd --no-create-home -u 1337 red40

FROM gcr.io/kctf-docker/challenge@sha256:d884e54146b71baf91603d5b73e563eaffc5a42d494b1e32341a5f76363060fb

COPY --from=chroot / /chroot
COPY nsjail.cfg  /opt/red40/

CMD kctf_setup && \
    kctf_drop_privs \
    socat \
    TCP-LISTEN:1337,reuseaddr,fork \
    EXEC:"kctf_pow nsjail --config /opt/red40/nsjail.cfg -- /bin/sh /opt/red40/entrypoint.sh"