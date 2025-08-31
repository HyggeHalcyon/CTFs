FROM ubuntu:24.04

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    gcc \
    make \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy source files
COPY ./src .

# Install Python dependencies
RUN pip3 install -r requirements.txt --break-system-packages

# # Compile bf.c with specified flags
# RUN gcc -fPIE -pie -Wl,-z,relro,-z,lazy bf.c -o bf

# # Make bf executable
# RUN chmod +x bf

# Copy flag file
COPY flag.txt /flag.txt
RUN chmod 444 /flag.txt

# Create non-root user for security
RUN useradd --system --no-create-home ctf

# Change ownership of app files to ctf user
RUN chown -R ctf:ctf /app

# Switch to non-root user
USER ctf

# Expose port
EXPOSE 5000

# Run Flask application
CMD ["python3", "app.py"]