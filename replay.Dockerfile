FROM ubuntu:24.04

# Install packages with apt
COPY apt-packages.txt /tmp/apt-packages.txt
RUN apt-get update && \
    apt-get install -y --no-install-recommends $(cat /tmp/apt-packages.txt | tr '\n' ' ')

# Clone and build TinyCC
RUN git clone https://repo.or.cz/tinycc.git

ENV TINYC_CFLAGS="-fsanitize=address -fno-omit-frame-pointer -O0 -g"
ENV TINYC_LDFLAGS="-fsanitize=address -static-libasan"
RUN cd /tinycc && \
    CFLAGS="${TINYC_CFLAGS}" LDFLAGS="${TINYC_LDFLAGS}" ./configure && \
    CFLAGS="${TINYC_CFLAGS}" LDFLAGS="${TINYC_LDFLAGS}" make && \
    make install PREFIX=/usr/local

# Copy replay code
COPY replay.py ./

CMD ["python3", "./replay.py"]