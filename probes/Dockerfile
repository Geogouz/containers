# Copyright European Organization for Nuclear Research (CERN) 2020
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Authors:
# - Eric Vaandering, <ewv@fnal.gov>, 2020

FROM almalinux:9

WORKDIR /tmp
ADD oic.rpm /tmp

RUN dnf install -y epel-release.noarch && \
    dnf install -y \
        git \
        gcc \
        libnsl \
        libaio \
        openssl-devel \
        procps-ng \
        python-devel \
        python-pip \
        make \
        go \
        tar \
        gzip \
        rsync \
        wget && \
    dnf clean all && \
    rm -rf /var/cache/dnf

RUN rpm -i https://download.oracle.com/otn_software/linux/instantclient/1923000/oracle-instantclient19.23-basic-19.23.0.0.0-1.aarch64.rpm; \
    echo "/usr/lib/oracle/19/client64/lib" >/etc/ld.so.conf.d/oracle.conf; \
    ldconfig

# Set Go environment variables
ENV GOPATH=/root/go
ENV GOBIN=$GOPATH/bin

# Create necessary directories
RUN mkdir -p $GOBIN && mkdir -p $GOPATH/src/github.com/dshearer

# Install dep (Go dependency management tool)
RUN curl https://raw.githubusercontent.com/golang/dep/master/install.sh | sh

# Download and extract the jobber tarball
RUN wget https://github.com/dshearer/jobber/archive/refs/tags/v1.4.0.tar.gz && \
    tar -xzf v1.4.0.tar.gz && \
    mv jobber-1.4.0 $GOPATH/src/github.com/dshearer/jobber && \
    cd $GOPATH/src/github.com/dshearer/jobber && \
    go mod init github.com/dshearer/jobber && \
    go mod tidy && \
    go mod vendor && \
    make && \
    make install

# Clean up
RUN rm -rf /tmp/*

RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN python3 -m pip install --no-cache-dir --upgrade setuptools
RUN rm -rf /usr/lib/python3.6/site-packages/ipaddress*
RUN python3 -m pip install --no-cache-dir --pre rucio[oracle,mysql,postgresql]
RUN python3 -m pip install --no-cache-dir j2cli psycopg2-binary
RUN python3 -m pip install --no-cache-dir cx-oracle PyMySQL

WORKDIR /
RUN git clone https://github.com/rucio/probes.git

ADD rucio.config.default.cfg /tmp/

ADD run-probes.sh /

ENTRYPOINT ["/run-probes.sh"]
