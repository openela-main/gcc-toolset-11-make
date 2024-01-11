# -*- coding: utf-8 -*-
%global __python /usr/bin/python3
%{?scl:%{?scl_package:%scl_package make}}
Summary: A GNU tool which simplifies the build process for users
Name: %{?scl_prefix}make
Epoch: 1
Version: 4.3
Release: 2%{?dist}
License: GPLv3+
URL: http://www.gnu.org/software/make/
Source: ftp://ftp.gnu.org/gnu/make/make-%{version}.tar.gz

%if 0%{?rhel} > 0
# This gives the user the option of saying --with guile, but defaults to WITHOUT
%bcond_with guile
%else
# This gives the user the option of saying --without guile, but defaults to WITH
%bcond_without guile
%endif

Patch0: make-4.3-getcwd.patch

# Assume we don't have clock_gettime in configure, so that
# make is not linked against -lpthread (and thus does not
# limit stack to 2MB).
Patch1: make-4.0-noclock_gettime.patch

# BZs #142691, #17374
Patch2: make-4.3-j8k.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1827850
# https://savannah.gnu.org/bugs/?58232
# Remove on next make rebase
Patch3: make-4.3-cloexec.patch

# autoreconf
BuildRequires: make
BuildRequires: autoconf, automake, gettext-devel
BuildRequires: procps
BuildRequires: perl-interpreter
%if %{with guile}
BuildRequires: pkgconfig(guile-2.2)
%endif
BuildRequires: gcc

%description
A GNU tool for controlling the generation of executables and other
non-source files of a program from the program's source files. Make
allows users to build and install packages without any significant
knowledge about the details of the build process. The details about
how the program should be built are provided for make in the program's
makefile.

%package devel
Summary: Header file for externally visible definitions

%description devel
The make-devel package contains gnumake.h.

%prep
%autosetup -p1 -n make-%{version}

rm -f tests/scripts/features/parallelism.orig

%build

%configure \
%if %{with guile}
    --with-guile
%else
    --without-guile
%endif

%make_build

%install
%make_install
ln -sf make ${RPM_BUILD_ROOT}/%{_bindir}/gmake
ln -sf make.1 ${RPM_BUILD_ROOT}/%{_mandir}/man1/gmake.1
rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir

%find_lang make

%check
echo ============TESTING===============
/usr/bin/env LANG=C make check && true
echo ============END TESTING===========

%files  -f make.lang
%license COPYING
%doc NEWS README AUTHORS
%{_bindir}/*
%{_mandir}/man*/*
%{_infodir}/*.info*
%{_includedir}/gnumake.h

%files devel
%{_includedir}/gnumake.h

%changelog
* Mon Jun 21 2021 Martin Cermak <mcermak@redhat.com> - 1:4.3-2
- CI gating related NVR bump and rebuild

* Thu Jun 10 2021 DJ Delorie <dj@redhat.com> - 1:4.3-1
- Initial sources for DTS 11 (#1958351)
