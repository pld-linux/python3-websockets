#
# Conditional build:
%bcond_without	doc	# API documentation

%define		module	websockets
Summary:	An implementation of the WebSocket Protocol for python with asyncio
Name:		python3-%{module}
Version:	9.0.2
Release:	3
License:	BSD-like
Group:		Libraries/Python
Source0:	https://github.com/aaugustin/websockets/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	af69f3188f6530acf4a79a901a698595
Patch0:		sphinx3.patch
URL:		https://pypi.python.org/pypi/websockets
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python3-sphinxcontrib-trio
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
websockets is a library for building WebSocket servers and clients in
Python with a focus on correctness and simplicity.

Built on top of asyncio, Python's standard asynchronous I/O framework,
it provides an elegant coroutine-based API.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%build
%py3_build

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
rm -rf docs/_build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a example/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/py.typed
%attr(755,root,root) %{py3_sitedir}/%{module}/*.so
%{py3_sitedir}/%{module}/__pycache__
%dir %{py3_sitedir}/%{module}/extensions
%{py3_sitedir}/%{module}/extensions/*.py
%{py3_sitedir}/%{module}/extensions/__pycache__
%dir %{py3_sitedir}/%{module}/legacy
%{py3_sitedir}/%{module}/legacy/*.py
%{py3_sitedir}/%{module}/legacy/__pycache__
%{py3_sitedir}/%{module}-%{version}-py*.egg-info
%{_examplesdir}/%{name}-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
