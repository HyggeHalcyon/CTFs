FROM ubuntu:22.04

RUN apt update && apt install -y socat dash

ENV PYTHONUNBUFFERED=1

RUN apt install -y python3 python3-pip

RUN pip install --upgrade pip setuptools
RUN pip install flask

EXPOSE 1337

RUN addgroup --system ctf && adduser --system --ingroup ctf ctf

WORKDIR /home/ctf

COPY challenge/ .
RUN mkdir -p /home/ctf/uploads
RUN chown -R ctf:ctf /home/ctf/uploads/

USER ctf

CMD ["./server.py"]
