FROM ubuntu:24.04@sha256:72297848456d5d37d1262630108ab308d3e9ec7ed1c3286a32fe09856619a782

ENV PROB_NAME prob
ENV PORT 13379

RUN apt-get update && apt-get install socat -y
RUN apt-get install gcc -y

RUN useradd --create-home --shell /bin/bash ctf

WORKDIR /home/ctf/

COPY ./deploy/run.sh ./run.sh
#COPY ./deploy/setup.sh ./setup.sh
COPY ./deploy/${PROB_NAME} ./${PROB_NAME}
COPY ./deploy/flag ./flag

#RUN chmod +x ./setup.sh
RUN chmod +x ./run.sh
#RUN ./setup.sh

RUN mkdir todo
RUN chown -R root:ctf /home/ctf
RUN chmod -R 750 /home/ctf
RUN chown -R ctf:ctf /home/ctf/todo
RUN chmod 444 /home/ctf/flag

EXPOSE ${PORT}
CMD socat -T60 -t60 TCP-LISTEN:${PORT},reuseaddr,fork EXEC:./run.sh,stderr
