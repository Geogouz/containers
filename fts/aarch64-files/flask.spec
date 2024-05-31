%define name Flask
%define version 1.1.4
%define unmangled_version 1.1.4
%define unmangled_version 1.1.4
%define release 1

Summary: A simple framework for building complex web applications.
Name: %{name}
Version: %{version}
Release: %{release}
Provides: python36-flask = %{version}-%{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: BSD-3-Clause
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Pallets <contact@palletsprojects.com>
Url: https://palletsprojects.com/p/flask/

%description
Flask is a lightweight `WSGI`_ web application framework. It is designed
to make getting started quick and easy, with the ability to scale up to
complex applications. It began as a simple wrapper around `Werkzeug`_
and `Jinja`_ and has become one of the most popular Python web
application frameworks.

Flask offers suggestions, but doesn't enforce any dependencies or
project layout. It is up to the developer to choose the tools and
libraries they want to use. There are many extensions provided by the
community that make adding new functionality easy.

%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
python3 setup.py build

%install
python3 setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
