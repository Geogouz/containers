%define name M2Crypto
%define version 0.35.2
%define unmangled_version 0.35.2
%define unmangled_version 0.35.2
%define release 1

Summary: M2Crypto: A Python crypto and SSL toolkit
Name: %{name}
Version: %{version}
Release: %{release}
Provides: python36-m2crypto = %{version}-%{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: MIT
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
Vendor: Matej Cepl <mcepl@cepl.eu>
Url: https://gitlab.com/m2crypto/m2crypto

%description
M2Crypto is the most complete Python wrapper for OpenSSL featuring RSA, DSA,
DH, EC, HMACs, message digests, symmetric ciphers (including AES); SSL
functionality to implement clients and servers; HTTPS extensions to Python's
httplib, urllib, and xmlrpclib; unforgeable HMAC'ing AuthCookies for web
session management; FTP/TLS client and server; S/MIME; M2Crypto can also be
used to provide SSL for Twisted. Smartcards supported through the Engine
interface.

%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
env CFLAGS="$RPM_OPT_FLAGS" python3 setup.py build

%install
python3 setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
