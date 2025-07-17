# Copyright European Organization for Nuclear Research (CERN) 2025
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
ARG RUCIO_EXTRAS="argcomplete"

# ----------------------------------------------------------------------------
# System packages
# ----------------------------------------------------------------------------
RUN dnf -y install yum-utils epel-release.noarch && \
    dnf upgrade -y && \
    yum-config-manager --enable crb && \
    dnf install -y \
        gfal2-all \
        python3-gfal2-util \
        python3-gfal2 \
        python3-pip \
        nordugrid-arc-client \
        nordugrid-arc-plugins-gfal \
        nordugrid-arc-plugins-globus \
        nordugrid-arc-plugins-s3 \
        nordugrid-arc-plugins-xrootd \
        voms-clients-java \
        xrootd-client && \
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
# • RUCIO_EXTRAS – The selected Rucio extras to install.
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel && \
    if [ -z "$RUCIO_REF" ]; then \
        # ------------------ Install released wheel from PyPI ----------------
        python3 -m pip install --no-cache-dir --pre \
            "rucio-clients[${RUCIO_EXTRAS}]==${TAG}"; \
    else \
        # ---------------- Build wheel from source, then install -------------
        dnf install -y git && \
        python3 -m pip install --no-cache-dir build && \
        git clone "${RUCIO_REPO}" /tmp/rucio && \
        cd /tmp/rucio && git checkout "${RUCIO_REF}" && \
        ./tools/build_sdist_wheel.sh clients && \
        WHEEL=$(realpath dist/$(ls dist | grep -E '^rucio_clients?-.*\.whl' | head -n1)) && \
        python3 -m pip install --no-cache-dir \
            "rucio-clients[${RUCIO_EXTRAS}] @ file://${WHEEL}" && \
        cd / && rm -rf /tmp/rucio && \
        dnf remove -y git && dnf autoremove -y && dnf clean all; \
    fi

# ----------------------------------------------------------------------------
# Additional runtime Python packages
# ----------------------------------------------------------------------------
RUN python3 -m pip install --no-cache-dir jinja2 j2cli pyyaml

# ----------------------------------------------------------------------------
# Non‑root user setup
# ----------------------------------------------------------------------------
# Add a separate user and change ownership of config dir to that user
RUN groupadd -g 1000 user && \
    useradd -ms /bin/bash -u 1000 -g 1000 user && \
    mkdir -p /opt/rucio/etc/ && \
    chown -R user:user /opt/rucio/etc/ && \
    mkdir -p /opt/user && \
    chown user:user /opt/user

USER user
WORKDIR /home/user

# ----------------------------------------------------------------------------
# Default configuration
# ----------------------------------------------------------------------------
ADD --chown=user:user rucio.default.cfg /opt/user/rucio.default.cfg
ADD init_rucio.sh /etc/profile.d/rucio_init.sh
ADD --chown=user:user ./entrypoint.sh /opt/user/entrypoint.sh

ENV PATH="/opt/rucio/bin:${PATH}"

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
ENTRYPOINT ["/opt/user/entrypoint.sh"]
CMD ["bash"]
