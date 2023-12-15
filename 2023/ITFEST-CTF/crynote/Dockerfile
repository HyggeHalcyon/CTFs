FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y xinetd
RUN groupadd -r ctf && useradd -r -g ctf ctf

ADD crynote /home/ctf/chall

RUN echo '#!/bin/bash\nservice xinetd restart && /bin/sleep infinity' > /etc/init.sh
RUN echo 'service ctf\n\ 
{\n\ 
    disable = no\n\ 
    socket_type = stream\n\ 
    protocol = tcp\n\ 
    wait = no\n\ 
    user = ctf\n\ 
    type = UNLISTED\n\ 
    port = 21337\n\ 
    bind = 0.0.0.0\n\ 
    server = /home/ctf/run\n\ 
}' > /etc/xinetd.d/ctf
RUN echo '#!/bin/bash\ncd /home/ctf && ./chall' > /home/ctf/run

RUN echo "STS23{__jgn_disubmit_ini_cuma_pajangan__}" > /home/ctf/flag.txt
RUN chmod 444 /home/ctf/flag.txt

RUN chmod 400 /etc/xinetd.d/ctf
RUN chmod 550 /home/ctf/chall /home/ctf/run /etc/init.sh

WORKDIR /home/ctf

RUN chown -R root:ctf /home/ctf
RUN service xinetd restart
