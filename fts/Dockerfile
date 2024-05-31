FROM centos:7

# Define an ARG for bypassing the cache
ARG CACHE_TS=1

RUN yum upgrade -y && \
    yum install -y yum-utils epel-release.noarch centos-release-scl && \
    yum-config-manager --save --setopt=epel.skip_if_unavailable=false && \
    echo 'skip_missing_names_on_install=0' >> /etc/yum.conf

ADD fts3-testing.repo /etc/yum.repos.d/fts3-testing.repo
RUN echo -e "[fts3-depend-el7]\nname=FTS3 Dependencies\nbaseurl=https://fts-repo.web.cern.ch/fts-repo/fts-depend/el7/x86_64\ngpgcheck=0\nenabled=1\nprotect=0" > /etc/yum.repos.d/fts3-depend-el7.repo
RUN echo -e "[dmc-el7]\nname=DMC Production Repository\nbaseurl=https://dmc-repo.web.cern.ch/dmc-repo/el7/x86_64\ngpgcheck=0\nenabled=1\nprotect=0" > /etc/yum.repos.d/dmc-el7.repo

# **************************************************
# Compile required libraries from the official repos

# Install supporting packages
RUN yum install -y gcc python36-devel mysql-devel rpm-build rpmdevtools wget

# Create RPM build environment
RUN rpmdev-setuptree

######################
# mysqlclient==1.4.6
######################
RUN wget https://files.pythonhosted.org/packages/d0/97/7326248ac8d5049968bf4ec708a5d3d4806e412a42e74160d7f266a3e03a/mysqlclient-1.4.6.tar.gz && \
    tar xzf mysqlclient-1.4.6.tar.gz
RUN cd mysqlclient-1.4.6 && \
    python3 setup.py bdist_rpm && \
    mv dist/mysqlclient-1.4.6-1.aarch64.rpm /tmp/ && \
    yum install -y /tmp/mysqlclient-1.4.6-1.aarch64.rpm && \
    rm -rf /mysqlclient-1.4.6 /tmp/mysqlclient-1.4.6-1.aarch64.rpm
#RUN python3 -c "import MySQLdb; print('Successfully imported MySQLdb!')"

######################
# SQLAlchemy==1.1.15
######################
RUN wget https://files.pythonhosted.org/packages/c2/f6/11fcc1ce19a7cb81b1c9377f4e27ce3813265611922e355905e57c44d164/SQLAlchemy-1.1.15.tar.gz && \
    tar xzf SQLAlchemy-1.1.15.tar.gz
RUN cd SQLAlchemy-1.1.15 && \
    python3 setup.py bdist_rpm && \
    mv dist/SQLAlchemy-1.1.15-1.aarch64.rpm /tmp/ && \
    yum install -y /tmp/SQLAlchemy-1.1.15-1.aarch64.rpm && \
    rm -rf /SQLAlchemy-1.1.15 /tmp/SQLAlchemy-1.1.15-1.aarch64.rpm
#RUN python3 -c "import sqlalchemy; print('Successfully imported sqlalchemy!')"

######################
# MarkupSafe==0.23
######################
RUN wget https://files.pythonhosted.org/packages/c0/41/bae1254e0396c0cc8cf1751cb7d9afc90a602353695af5952530482c963f/MarkupSafe-0.23.tar.gz -O /root/rpmbuild/SOURCES/MarkupSafe-0.23.tar.gz

# We use custom SPECS to set the name required by other packages
COPY aarch64-files/MarkupSafe.spec /root/rpmbuild/SPECS/
RUN rpmbuild -ba /root/rpmbuild/SPECS/MarkupSafe.spec && \
    mv /root/rpmbuild/RPMS/aarch64/MarkupSafe-0.23-1.aarch64.rpm /tmp/ && \
    yum install -y /tmp/MarkupSafe-0.23-1.aarch64.rpm
#RUN python3 -c "import markupsafe; print('Successfully imported markupsafe!')"

######################
# Jinja2==2.11.1
######################
RUN wget https://files.pythonhosted.org/packages/d8/03/e491f423379ea14bb3a02a5238507f7d446de639b623187bccc111fbecdf/Jinja2-2.11.1.tar.gz && \
    tar xzf Jinja2-2.11.1.tar.gz
RUN cd Jinja2-2.11.1 && \
    python3 setup.py bdist_rpm && \
    mv dist/Jinja2-2.11.1-1.noarch.rpm /tmp/ && \
    yum install -y /tmp/Jinja2-2.11.1-1.noarch.rpm && \
    rm -rf /Jinja2-2.11.1 /tmp/Jinja2-2.11.1-1.noarch.rpm
#RUN python3 -c "import jinja2; print('Successfully imported jinja2!')"

######################
# Werkzeug==1.0.1
######################
RUN wget https://files.pythonhosted.org/packages/10/27/a33329150147594eff0ea4c33c2036c0eadd933141055be0ff911f7f8d04/Werkzeug-1.0.1.tar.gz && \
    tar xzf Werkzeug-1.0.1.tar.gz
RUN cd Werkzeug-1.0.1 && \
    python3 setup.py bdist_rpm && \
    mv dist/Werkzeug-1.0.1-1.noarch.rpm /tmp/ && \
    yum install -y /tmp/Werkzeug-1.0.1-1.noarch.rpm && \
    rm -rf /Werkzeug-1.0.1 /tmp/Werkzeug-1.0.1-1.noarch.rpm
#RUN python3 -c "import werkzeug; print('Successfully imported werkzeug!')"

######################
# itsdangerous==1.1.0
######################
RUN wget https://files.pythonhosted.org/packages/68/1a/f27de07a8a304ad5fa817bbe383d1238ac4396da447fa11ed937039fa04b/itsdangerous-1.1.0.tar.gz && \
    tar xzf itsdangerous-1.1.0.tar.gz
RUN cd itsdangerous-1.1.0 && \
    python3 setup.py bdist_rpm && \
    mv dist/itsdangerous-1.1.0-1.noarch.rpm /tmp/ && \
    yum install -y /tmp/itsdangerous-1.1.0-1.noarch.rpm && \
    rm -rf /itsdangerous-1.1.0 /tmp/itsdangerous-1.1.0-1.noarch.rpm
#RUN python3 -c "import itsdangerous; print('Successfully imported itsdangerous!')"

######################
# click==6.7
######################
RUN wget https://files.pythonhosted.org/packages/95/d9/c3336b6b5711c3ab9d1d3a80f1a3e2afeb9d8c02a7166462f6cc96570897/click-6.7.tar.gz && \
    tar xzf click-6.7.tar.gz
RUN cd click-6.7 && \
    python3 setup.py bdist_rpm && \
    mv dist/click-6.7-1.noarch.rpm /tmp/ && \
    yum install -y /tmp/click-6.7-1.noarch.rpm && \
    rm -rf /click-6.7 /tmp/click-6.7-1.noarch.rpm
#RUN python3 -c "import click; print('Successfully imported click!')"

######################
# python36-flask==1.1.4
######################
RUN wget https://files.pythonhosted.org/packages/4d/5b/2d145f5fe718b2f15ebe69240538f06faa8bbb76488bf962091db1f7a26d/Flask-1.1.4.tar.gz -O /root/rpmbuild/SOURCES/Flask-1.1.4.tar.gz

# We use custom SPECS to set the name required by other packages
COPY aarch64-files/flask.spec /root/rpmbuild/SPECS/
RUN rpmbuild -ba /root/rpmbuild/SPECS/flask.spec && \
    mv /root/rpmbuild/RPMS/noarch/Flask-1.1.4-1.noarch.rpm /tmp/ && \
    yum install -y /tmp/Flask-1.1.4-1.noarch.rpm
#RUN python3 -c "import flask; print('Successfully imported flask!')"

######################
# M2Crypto==0.35.2
######################
RUN wget https://files.pythonhosted.org/packages/74/18/3beedd4ac48b52d1a4d12f2a8c5cf0ae342ce974859fba838cbbc1580249/M2Crypto-0.35.2.tar.gz -O /root/rpmbuild/SOURCES/M2Crypto-0.35.2.tar.gz

# We use custom SPECS to set the name required by other packages
COPY aarch64-files/m2crypto.spec /root/rpmbuild/SPECS/
RUN rpmbuild -ba /root/rpmbuild/SPECS/m2crypto.spec && \
    mv /root/rpmbuild/RPMS/aarch64/M2Crypto-0.35.2-1.aarch64.rpm /tmp/ && \
    yum install -y /tmp/M2Crypto-0.35.2-1.aarch64.rpm
#RUN python3 -c "import M2Crypto; print('Successfully imported M2Crypto!')"
# **************************************************


# Download, install and clean the required core dependencies
RUN wget https://buildlogs.centos.org/c7-rh-python36.aarch64/rh-python36/20181031211245/2.0-1.el7.aarch64/rh-python36-runtime-2.0-1.el7.aarch64.rpm && \
    wget https://buildlogs.centos.org/c7-rh-python36.aarch64/rh-python36-python-setuptools/20181101145603/36.5.0-1.el7.aarch64/rh-python36-python-setuptools-36.5.0-1.el7.noarch.rpm && \
    wget https://cbs.centos.org/kojifiles/packages/httpd24-httpd/2.4.6/25.bs1.el7/aarch64/httpd24-httpd-tools-2.4.6-25.bs1.el7.aarch64.rpm && \
    wget https://cbs.centos.org/kojifiles/packages/httpd24/1.1/19.el7/aarch64/httpd24-runtime-1.1-19.el7.aarch64.rpm && \
    wget https://cbs.centos.org/kojifiles/packages/httpd24-httpd/2.4.6/25.bs1.el7/aarch64/httpd24-httpd-2.4.6-25.bs1.el7.aarch64.rpm && \
    wget https://cbs.centos.org/kojifiles/packages/rh-python36-mod_wsgi/4.5.18/1.bs1.el7/aarch64/rh-python36-mod_wsgi-4.5.18-1.bs1.el7.aarch64.rpm

RUN yum install -y rh-python36-runtime-2.0-1.el7.aarch64.rpm && \
    yum install -y rh-python36-python-setuptools-36.5.0-1.el7.noarch.rpm && \
    yum install -y httpd24-httpd-tools-2.4.6-25.bs1.el7.aarch64.rpm && \
    yum install -y httpd24-runtime-1.1-19.el7.aarch64.rpm && \
    yum install -y httpd24-httpd-2.4.6-25.bs1.el7.aarch64.rpm && \
    yum install -y rh-python36-mod_wsgi-4.5.18-1.bs1.el7.aarch64.rpm

RUN rm -f  \
    rh-python36-runtime-2.0-1.el7.aarch64.rpm \
    rh-python36-python-setuptools-36.5.0-1.el7.noarch.rpm \
    httpd24-httpd-tools-2.4.6-25.bs1.el7.aarch64.rpm \
    httpd24-runtime-1.1-19.el7.aarch64.rpm \
    httpd24-httpd-2.4.6-25.bs1.el7.aarch64.rpm \
    rh-python36-mod_wsgi-4.5.18-1.bs1.el7.aarch64.rpm

# Install required packages
RUN yum install -y \
    mysql \
    multitail \
    gfal2-plugin* \
    fts-libs \
    fts-server \
    fts-rest-server-3.13.0-r2405271058git798429f.el7.cern.noarch \
    fts-monitoring \
    fts-mysql \
    fts-msg \
    zeromq
RUN yum clean all

# Database configuration for FTS server
COPY fts3config /etc/fts3/fts3config
RUN chmod +x /usr/share/fts/fts-database-upgrade.py

# Configuration for FTSREST and FTSMON
COPY fts3rest.conf /etc/httpd/conf.d/fts3rest.conf
COPY fts3restconfig /etc/fts3/fts3restconfig
RUN echo "" > /etc/httpd/conf.d/ssl.conf &&\
    echo "" > /etc/httpd/conf.d/autoindex.conf &&\
    echo "" > /etc/httpd/conf.d/userdir.conf &&\
    echo "" > /etc/httpd/conf.d/welcome.conf &&\
    echo "" > /etc/httpd/conf.d/zgridsite.conf

# FTS monitoring ActiveMQ configuration
COPY fts-msg-monitoring.conf /etc/fts3/fts-msg-monitoring.conf

# Entrypoint waiting script for MySQL
COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Shortcut for logfiles
COPY logshow /usr/local/bin/logshow
RUN chmod +x /usr/local/bin/logshow
RUN touch /var/log/fts3/fts3server.log
RUN chown -R fts3:fts3 /var/log/fts3/fts3server.log
RUN touch /var/log/fts3rest/fts3rest.log
RUN chown -R fts3:fts3 /var/log/fts3rest

# Startup
EXPOSE 8446 8449
ADD docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
