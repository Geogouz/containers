# Copyright European Organization for Nuclear Research (CERN) 2023
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

FROM almalinux:9 as rpm_builder

RUN dnf upgrade -y
RUN dnf install -y rpm-build rpmdevtools yum-utils epel-release.noarch
RUN yum-config-manager --enable crb

# Conditional execution based on architecture
RUN if [ "$(uname -m)" != "aarch64" ]; then  \
    echo "Non-arm64 architecture detected, building OpenSSL from source and rebuilding davix"; \
    # BUILD and install openssl 3.1
    ADD openssl.spec /root/rpmbuild/SPECS/openssl.spec; \
    yum-builddep -y /root/rpmbuild/SPECS/openssl.spec; \
    spectool -g /root/rpmbuild/SPECS/openssl.spec --directory /root/rpmbuild/SOURCES/; \
    rpmbuild -bb /root/rpmbuild/SPECS/openssl.spec; \
    dnf install -y /root/rpmbuild/RPMS/*/*; \
    # REBUILD davix to use openssl 3.1
    yumdownloader --source davix; \
    yum-builddep -y --srpm davix*.src.rpm; \
    rpmbuild --rebuild davix-*.src.rpm; \
else \
    echo "arm64 architecture detected, skipping custom OpenSSL build"; \
    dnf install -y openssl-3.1.4 \
fi

FROM almalinux:9

ARG TAG

WORKDIR /tmp

RUN dnf install -y epel-release.noarch && \
    dnf upgrade -y && \
    dnf install -y \
        fetch-crl \
        gfal2-plugin-file \
        gfal2-plugin-gridftp \
        gfal2-plugin-http \
        gfal2-plugin-srm \
        gfal2-plugin-xrootd \
        libnsl \
        libaio \
        patch \
        python-gfal2 \
        procps-ng \
        python-pip \
        python-mod_wsgi \
        sendmail \
        sendmail-cf \
        memcached \
        patchutils \
        xrootd-client && \
    dnf clean all && \
    rm -rf /var/cache/dnf
RUN rpm -i https://download.oracle.com/otn_software/linux/instantclient/1912000/oracle-instantclient19.12-basiclite-19.12.0.0.0-1.x86_64.rpm; \
    echo "/usr/lib/oracle/19/client64/lib" >/etc/ld.so.conf.d/oracle.conf; \
    ldconfig

# Set default environment variable that can be overridden
ENV USE_DAVIX_WITH_OPENSSL31=False

# Install additional packages for arm64 architecture and set environment variables conditionally
RUN if [ "$(uname -m)" = "aarch64" ]; then \
        dnf install -y gcc python3-devel && \
        dnf clean all && \
        rm -rf /var/cache/dnf; \
    else \
        USE_DAVIX_WITH_OPENSSL31=True; \
    fi

# TODO: The following step is required for custom building cases (i.e. non arm64)
#COPY --from=rpm_builder /root/rpmbuild/RPMS/x86_64/*.rpm /tmp/rpms/

RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir --upgrade setuptools && \
    python3 -m pip install --no-cache-dir --pre rucio[oracle,mysql,postgresql,globus]==$TAG && \
    python3 -m pip install --no-cache-dir j2cli

ADD rucio.config.default.cfg /tmp/
ADD start-daemon.sh /

RUN update-crypto-policies --set DEFAULT:SHA1

RUN mkdir /var/log/rucio

VOLUME /var/log/rucio
VOLUME /opt/rucio/etc

ENTRYPOINT ["/start-daemon.sh"]
