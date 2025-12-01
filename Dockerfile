FROM ubuntu:24.04

# Install packages with apt
COPY apt-packages.txt /tmp/apt-packages.txt
RUN apt-get update && \
    apt-get install -y --no-install-recommends $(cat /tmp/apt-packages.txt | tr '\n' ' ')

# Clone and build TinyCC
RUN git clone https://repo.or.cz/tinycc.git && cd /tinycc && git checkout ab2ce3b13ac96cb6c221ecb5cc5e6ed2d25cbd14

ENV TINYC_CFLAGS="-fsanitize=address -fno-omit-frame-pointer -fprofile-arcs -ftest-coverage -O0 -g"
ENV TINYC_LDFLAGS="-fsanitize=address -static-libasan -lgcov"
RUN cd /tinycc && \
    CFLAGS="${TINYC_CFLAGS}" LDFLAGS="${TINYC_LDFLAGS}" ./configure && \
    CFLAGS="${TINYC_CFLAGS}" LDFLAGS="${TINYC_LDFLAGS}" make && \
    make install PREFIX=/usr/local

# Install Python dependencies
COPY requirements.txt ./
RUN python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

# Copy fuzzer code
COPY fuzzer fuzzer
COPY run_and_get_coverage.sh ./

# Default evaluation time (can be overridden at runtime with -e EVALUATION_TIME=<value>)
ENV EVALUATION_TIME=3600
# Set to enable seeds (e.g. -e PROVIDE_SEEDS=1)
ENV PROVIDE_SEEDS=""

CMD ["/bin/bash", "./run_and_get_coverage.sh"]