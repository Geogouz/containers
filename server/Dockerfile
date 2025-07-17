# Copyright European Organization for Nuclear Research (CERN) 2017
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

FROM almalinux:9

# ----------------------------------------------------------------------------
# Build‑time parameters
# ----------------------------------------------------------------------------
ARG TAG
ARG RUCIO_REF
ARG RUCIO_REPO="https://github.com/rucio/rucio.git"
ARG RUCIO_EXTRAS="oracle,mysql,postgresql"

WORKDIR /tmp

# ----------------------------------------------------------------------------
# System packages
# ----------------------------------------------------------------------------
RUN dnf install -y epel-release.noarch && \
    dnf upgrade -y && \
    dnf install -y \
        gridsite \
        patch \
        procps-ng \
        python3-pip \
        python3-mod_wsgi \
        memcached \
        patchutils && \
    dnf clean all && \
    rm -rf /var/cache/dnf

# ----------------------------------------------------------------------------
# Upgrade toolchain and install (or build) rucio‑clients
# ----------------------------------------------------------------------------
# • TAG          – The version/release tag to install from PyPI (e.g. 37.0.0).
# • RUCIO_REF    – The Git ref (commit, branch, or tag).
#                  If empty      → install the published wheel from PyPI.
#                  If non‑empty  → build Rucio from that ref and install the resulting wheel.
# • RUCIO_REPO   – The Rucio Git URL to clone when building from source (when RUCIO_REF is set).
#                  It points to the official Rucio repository (but can be changed manually).
# • RUCIO_EXTRAS – The selected Rucio extras to install. \
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel && \
    if [ -z "$RUCIO_REF" ]; then \
        # ------------------ Install released wheel from PyPI ----------------
        python3 -m pip install --no-cache-dir --pre \
            "rucio[${RUCIO_EXTRAS}]==${TAG}"; \
    else \
        # ---------------- Build wheel from source, then install -------------
        dnf install -y git && \
        python3 -m pip install --no-cache-dir build && \
        git clone "${RUCIO_REPO}" /tmp/rucio && \
        cd /tmp/rucio && git checkout "${RUCIO_REF}" && \
        ./tools/build_sdist_wheel.sh rucio && \
        WHEEL=$(realpath dist/$(ls dist | grep -E '^rucio-.*\.whl' | head -n1)) && \
        python3 -m pip install --no-cache-dir \
            "rucio[${RUCIO_EXTRAS}] @ file://${WHEEL}" && \
        cd / && rm -rf /tmp/rucio && \
        dnf remove -y git && dnf autoremove -y && dnf clean all; \
    fi

# ----------------------------------------------------------------------------
# Additional runtime Python packages
# ----------------------------------------------------------------------------
RUN python3 -m pip install --no-cache-dir j2cli

# ----------------------------------------------------------------------------
# Rucio/web‑server configuration
# ----------------------------------------------------------------------------
ADD gacl /etc/httpd/
ADD rucio.config.default.cfg /tmp/
ADD rucio.conf.j2 /tmp/
ADD httpd.conf.j2 /tmp/
ADD 00-mpm.conf.j2 /tmp/
ADD docker-entrypoint.sh /
ADD robots.txt /var/www/html

# Update Apache configs
RUN rm /etc/httpd/conf.d/zgridsite.conf \
       /etc/httpd/conf.d/welcome.conf \
       /etc/httpd/conf.d/userdir.conf \
       /etc/httpd/conf.d/ssl.conf && \
    # Rucio log directories
    mkdir -p /var/log/rucio/trace && chown apache:apache /var/log/rucio/trace && \
    mkdir -p /var/log/rucio/nongrid_trace && chown apache:apache /var/log/rucio/nongrid_trace

RUN update-crypto-policies --set DEFAULT:SHA1

VOLUME /var/log/httpd
VOLUME /opt/rucio/etc

EXPOSE 80
EXPOSE 443

# ----------------------------------------------------------------------------
# Optional policy‑specific Python packages
# ----------------------------------------------------------------------------
ARG POLICY_PACKAGE_REQUIREMENTS
ARG USER=root
USER root
RUN if [ -n "$POLICY_PACKAGE_REQUIREMENTS" ]; then \
        dnf install -y git && \
        for package in $(echo $POLICY_PACKAGE_REQUIREMENTS | tr "," "\n"); do \
            python3 -m pip install --no-cache-dir $package; \
        done; \
        dnf remove -y git && dnf autoremove && dnf clean all; \
    fi
USER ${USER}

# ----------------------------------------------------------------------------
# Runtime
# ----------------------------------------------------------------------------
ENTRYPOINT ["/docker-entrypoint.sh"]
