# Copyright European Organization for Nuclear Research (CERN) 2020
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Authors:
# - Eric Vaandering, <ewv@fnal.gov>, 2020

FROM almalinux:9

# ----------------------------------------------------------------------------
# Build‑time parameters
# ----------------------------------------------------------------------------
ARG TAG
ARG RUCIO_REF
ARG RUCIO_REPO="https://github.com/rucio/rucio.git"
ARG RUCIO_EXTRAS="oracle,mysql,postgresql"
ARG PROBES_REF
ARG PROBES_REPO="https://github.com/rucio/probes.git"

WORKDIR /tmp
ADD oic.rpm /tmp

# ----------------------------------------------------------------------------
# System packages
# ----------------------------------------------------------------------------
RUN dnf install -y epel-release.noarch && \
    dnf upgrade -y && \
    dnf install -y \
        git \
        openssl-devel \
        procps-ng \
        python3-devel \
        python3-pip && \
    dnf clean all && \
    rm -rf /var/cache/dnf

# ----------------------------------------------------------------------------
# Job scheduler (jobber)
# ----------------------------------------------------------------------------
RUN rpm -i https://github.com/dshearer/jobber/releases/download/v1.4.0/jobber-1.4.0-1.el7.x86_64.rpm

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
        # ------------ Install released wheel (TAG) or latest (no TAG) -------
        if [ -n "$TAG" ]; then \
            python3 -m pip install --no-cache-dir --pre \
                "rucio[${RUCIO_EXTRAS}]==${TAG}"; \
        else \
            echo "No TAG supplied – installing latest pre‑release from PyPI" && \
            python3 -m pip install --no-cache-dir --pre \
                "rucio[${RUCIO_EXTRAS}]"; \
        fi; \
    else \
        # ---------------- Build wheel from source, then install -------------
        python3 -m pip install --no-cache-dir build && \
        git clone "${RUCIO_REPO}" /tmp/rucio && \
        cd /tmp/rucio && git checkout "${RUCIO_REF}" && \
        ./tools/build_sdist_wheel.sh rucio && \
        WHEEL=$(realpath dist/$(ls dist | grep -E '^rucio-.*\.whl' | head -n1)) && \
        python3 -m pip install --no-cache-dir \
            "rucio[${RUCIO_EXTRAS}] @ file://${WHEEL}" && \
        cd / && rm -rf /tmp/rucio && \
        dnf clean all; \
    fi

# ----------------------------------------------------------------------------
# Additional runtime Python packages
# ----------------------------------------------------------------------------
RUN python3 -m pip install --no-cache-dir \
        j2cli \
        psycopg2-binary \
        oracledb \
        PyMySQL

# ----------------------------------------------------------------------------
# Get probes source
# ----------------------------------------------------------------------------
WORKDIR /
RUN git clone "${PROBES_REPO}" /probes && \
    if [ -n "$PROBES_REF" ]; then \
        cd /probes && git checkout "${PROBES_REF}"; \
    fi

# ---------------------------------------------------------------------------
# Configuration & entrypoint
# ---------------------------------------------------------------------------
ADD rucio.config.default.cfg /tmp/
ADD run-probes.sh /

ENTRYPOINT ["/run-probes.sh"]
