from python:3.13.5-slim AS app

RUN pip install --no-cache-dir capstone

# RUN apt-get update && \
#         apt-get -y install socat

## gdbserver juste for debugging 
RUN apt-get update && \
        apt-get install -y gdb gdbserver && \
        apt-get -y install socat && \
        apt-get -y install procps


RUN adduser nobody2

COPY ./main.py /app/run


COPY flag.txt libc.so.6* ld-linux-x86-64.so.2* app/



RUN chmod 755 /app/run
RUN chmod 444 /app/flag.txt

user nobody2
CMD socat TCP-LISTEN:5000,reuseaddr,fork EXEC:/app/run