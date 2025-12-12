%define libname	%mklibname %{name}
%define devname	%mklibname %{name} -d
%define pyname	python-%{name}

%bcond check	0

Summary:	A plain-C implementation of Google's Protocol Buffers data format
Name:		nanopb
Version:	0.4.9.1
Release:	2
License:	Zlib
Group:		System/Libraries
URL:		https://jpa.kapsi.fi/nanopb/
Source0:	https://github.com/nanopb/nanopb/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:	cmake ninja
BuildRequires:	pkgconfig(protobuf)
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(poetry)
%if %{with check}
BuildRequires:	scons
BuildRequires:	python%{pyver}dist(scons)
BuildRequires:	python%{pyver}dist(grpcio)
%endif

%description
Nanopb is a small code-size Protocol Buffers implementation in ansi C. It is
especially suitable for use in microcontrollers, but fits any memory restricted
system.

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:	A plain-C implementation of Google's Protocol Buffers data format
Group:		System/Libraries

%description -n	%{libname}
Nanopb is a small code-size Protocol Buffers implementation in ansi C. It is
especially suitable for use in microcontrollers, but fits any memory restricted
system.

%files -n %{libname}
%license LICENSE.txt
%{_libdir}/libprotobuf-nanopb.so.*

#---------------------------------------------------------------------------

%package -n %{devname}
Summary:	Headers, libraries and docs for the %{name} library
Group:		Development/C
Requires:	%{libname} = %{EVRD}

%description -n	%{devname}
Nanopb is a small code-size Protocol Buffers implementation in ansi C. It is
especially suitable for use in microcontrollers, but fits any memory restricted
system.

This package contains header files and development libraries needed to
develop programs using the %{name} library.

%files -n %{devname}
%license LICENSE.txt
%doc README.md
%{_includedir}/nanopb/
%{_libdir}/libprotobuf-nanopb.so
%dir %{_libdir}/cmake/nanopb
%{_libdir}/cmake/nanopb/*.cmake

#---------------------------------------------------------------------------

%package -n %{pyname}
Summary:	A python implementation of Google's Protocol Buffers data format
Requires:	%{libname} = %{EVRD}

%description -n %{pyname}
Nanopb is a small code-size Protocol Buffers implementation in ansi C. It is
especially suitable for use in microcontrollers, but fits any memory restricted
system.

This package contains a python implementation of %{name}.

%files -n %{pyname}
%{_bindir}/nanopb_generator
%{_bindir}/protoc-gen-nanopb
%{py_puresitedir}/*

#---------------------------------------------------------------------------

%prep
%autosetup -p1
# remove unneeded files
rm generator/{nanopb_generator.py2,protoc-gen-nanopb-py2}
rm generator/*.bat

# https://github.com/nanopb/nanopb/blob/master/extra/poetry/poetry_build.sh
cp extra/poetry/pyproject.toml .
mkdir -p nanopb
cp -r generator nanopb
touch nanopb/__init__.py nanopb/generator/__init__.py
make -C nanopb/generator/proto

%build
%cmake \
	-Dnanopb_BUILD_GENERATOR:BOOL=OFF \
	-GNinja
cd ..

%ninja_build -C build
%py_build

%install
%ninja_install -C build
%py_install

%if %{with check}
%check
pushd tests
scons
popd
%endif

