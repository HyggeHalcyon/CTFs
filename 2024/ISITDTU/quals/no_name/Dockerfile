FROM ubuntu:22.04 AS builder
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y make git python3 ninja-build gcc pkg-config libglib2.0-dev
RUN git clone https://github.com/qemu/qemu /qemu
WORKDIR /qemu
COPY patch.diff .
RUN git checkout e86e00a2493254d072581960b48461eb96481e45
RUN git apply < patch.diff
RUN ./configure --disable-system --enable-linux-user --disable-bpf --static
RUN make -j$((`nproc`-1)) qemu-aarch64

# Create the final image
FROM ubuntu:22.04
RUN apt update && apt install -y libc6-arm64-cross socat
RUN useradd -m ctf
WORKDIR /challenge


COPY --from=builder /qemu/build/qemu-aarch64 qemu_aarch64
COPY chall chall
COPY flag flag
RUN chown -R ctf:ctf /challenge && chmod -R 750 /challenge && chmod 440 /challenge/flag && chmod 550 /challenge

USER ctf
ENTRYPOINT ["socat", "tcp-l:1337,reuseaddr,fork", "EXEC:./qemu_aarch64 -L /usr/aarch64-linux-gnu/ ./chall,stderr"]
EXPOSE 1337