FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y socat coreutils && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m tempuser

WORKDIR /app

COPY runner /app/runner
COPY sandbox /app/sandbox
COPY flag.txt /flagggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg.txt

RUN chmod +x /app/runner && \
    chown tempuser:tempuser /app/runner && \
    chmod +x /app/sandbox && \
    chown tempuser:tempuser /app/sandbox

USER tempuser

EXPOSE 10002

CMD ["sh", "-c", "socat -d -d TCP4-LISTEN:10002,reuseaddr,fork EXEC:'/app/sandbox /app/runner',pty,stderr,setsid,sigint,sane"]