FROM debian:latest

RUN apt-get update && apt-get install -y xinetd make g++ && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*
RUN useradd -U -m -s /bin/bash ctf

# COPY ./xinetd.conf /etc/xinetd.conf
# RUN chmod 644 /etc/xinetd.conf

# COPY ./chall.cpp /home/ctf/chall.cpp
# COPY ./Makefile /home/ctf/Makefile
# COPY ./run.sh /home/ctf/run
# COPY ./flag.txt /home/ctf/flag.txt
# COPY ./startchall.sh /usr/bin/startchall
# COPY ./xinetd /etc/xinetd.d/xinetd

# RUN chown -R root:ctf /home/ctf && chmod -R 550 /home/ctf
# RUN chmod 500 /etc/xinetd.d/xinetd && chmod 500 /usr/bin/startchall
# WORKDIR /home/ctf/
# RUN make
# RUN apt-get purge -y g++ make

CMD ["/usr/bin/startchall"]
