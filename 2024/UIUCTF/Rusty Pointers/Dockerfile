FROM ubuntu:20.04

# Install dependencies
# according to docker, apt isn't stable in CLI, so use apt-get.

# Initialize User
RUN mkdir -p /usr/src/pwn
WORKDIR /usr/src/pwn

# Copy flag
COPY flag.txt .
RUN chmod 444 flag.txt

# Set up pwn user
RUN adduser --disabled-password --gecos "" pwn

# Switch to pwn user
USER pwn

# Keep the container running
CMD tail -f /dev/null
