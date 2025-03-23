FROM ubuntu:22.04
RUN apt update && apt install socat -y
RUN groupadd -r ctf && useradd -r -g ctf ctf
WORKDIR /home/ctf
EXPOSE 9004

COPY flag.txt .
COPY precision .
COPY libc.so.6 .
COPY ld-linux-x86-64.so.2 .
RUN chmod +x precision
RUN chmod +x libc.so.6
RUN chmod +x ld-linux-x86-64.so.2


CMD ["socat", "tcp-l:9004,reuseaddr,fork", "EXEC:./precision"]