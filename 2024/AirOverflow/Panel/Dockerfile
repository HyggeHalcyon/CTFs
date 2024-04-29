FROM theflash2k/pwn-chal:latest
ENV CHAL_NAME=panel
COPY ${CHAL_NAME} .
EXPOSE 8000

# For dynamic flagging:
COPY docker-entrypoint.sh /tmp/docker-entrypoint.sh
RUN chmod +x /tmp/docker-entrypoint.sh
ENTRYPOINT [ "/tmp/docker-entrypoint.sh" ]