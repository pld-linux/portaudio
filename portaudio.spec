#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
%bcond_without	apidocs		# documentation generated with doxygen
%bcond_without	asihpi		# ASI HPI support

Summary:	Free, cross platform, open-source, audio I/O library
Summary(pl.UTF-8):	Darmowa, międzyplatformowa i otwarta biblioteka I/O audio
Name:		portaudio
%define	fdate	20210406
%define	fver	190700
Version:	19.7.0.%{fdate}
Release:	1
License:	MIT-like (see LICENSE.txt)
Group:		Libraries
Source0:	http://files.portaudio.com/archives/pa_stable_v%{fver}_%{fdate}.tgz
# Source0-md5:	ad319249932c6794b551d954b8844402
Patch0:		%{name}-ac.patch
URL:		http://www.portaudio.com/
BuildRequires:	alsa-lib-devel >= 0.9
BuildRequires:	autoconf >= 2.13
BuildRequires:	automake
%{?with_apidocs:BuildRequires:	doxygen}
%{?with_asihpi:BuildRequires:	hpklinux-devel >= 4.06}
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.566
%{?with_asihpi:Requires:	hpklinux-libs >= 4.06}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PortAudio is a free, cross platform, open-source, audio I/O library.
It lets you write simple audio programs in 'C' that will compile and
run on many platforms including Windows, Macintosh (8,9,X), Unix
(OSS), SGI, and BeOS.

%description -l pl.UTF-8
PortAudio to darmowa, międzyplatformowa i otwarta biblioteka I/O
audio. Pozwala na pisanie prostych programów w "C", które będą się
kompilować i uruchamiać na wielu platformach, w tym Windows, Macintosh
(8,9,X), Unix (OSS), SGI, i BeOS.

%package devel
Summary:	Header files for PortAudio library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki PortAudio
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	alsa-lib-devel >= 0.9
%{?with_asihpi:Requires:	hpklinux-devel >= 4.06}
Requires:	jack-audio-connection-kit-devel

%description devel
Header files for PortAudio library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki PortAudio.

%package static
Summary:	Static PortAudio library
Summary(pl.UTF-8):	Statyczna biblioteka PortAudio
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static PortAudio library.

%description static -l pl.UTF-8
Statyczna biblioteka PortAudio.

%package apidocs
Summary:	portaudio API documentation
Summary(pl.UTF-8):	Documentacja API portaudio
Group:		Documentation
BuildArch:	noarch

%description apidocs
Documentation for portaudio API in HTML format generated from
portaudio sources by doxygen.

%description apidocs -l pl.UTF-8
Dokumentacja API portaudio w formacie HTML generowane ze źrodeł
portaudio przez doxygen.

%package c++
Summary:	C++ binding for PortAudio library
Summary(pl.UTF-8):	Wiązanie C++ do biblioteki PortAudio
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description c++
C++ binding for PortAudio library.

%description c++ -l pl.UTF-8
Wiązanie C++ do biblioteki PortAudio.

%package c++-devel
Summary:	Header files for C++ binding for PortAudio library
Summary(pl.UTF-8):	Pliki nagłówkowe wiązania C++ do biblioteki PortAudio
Group:		Development/Libraries
Requires:	%{name}-c++ = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	libstdc++-devel

%description c++-devel
Header files for C++ binding for PortAudio library.

%description c++-devel -l pl.UTF-8
Pliki nagłówkowe wiązania C++ do biblioteki PortAudio.

%package c++-static
Summary:	Static library of C++ binding for PortAudio library
Summary(pl.UTF-8):	Statyczna biblioteka wiązania C++ do biblioteki PortAudio
Group:		Development/Libraries
Requires:	%{name}-c++-devel = %{version}-%{release}

%description c++-static
Static library of C++ binding for PortAudio library.

%description c++-static -l pl.UTF-8
Statyczna biblioteka wiązania C++ do biblioteki PortAudio.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
cp -f /usr/share/automake/config.sub .
%{__libtoolize}
cd bindings/cpp
%{__aclocal}
%{__autoconf}
%{__automake}
cd ../..
%{__aclocal}
%{__autoconf}
%configure \
	--enable-cxx \
	--enable-static%{!?with_static_libs:=no} \
	%{!?with_asihpi:--without-asihpi}

%{__make} -j1
%{?with_apidocs:/usr/bin/doxygen}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	c++ -p /sbin/ldconfig
%postun	c++ -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md LICENSE.txt
%attr(755,root,root) %{_libdir}/libportaudio.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libportaudio.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libportaudio.so
%{_includedir}/pa_jack.h
%{_includedir}/pa_linux_alsa.h
%{_includedir}/portaudio.h
%{_pkgconfigdir}/portaudio-2.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libportaudio.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
%endif

%files c++
%defattr(644,root,root,755)
%doc bindings/cpp/{COPYING,ChangeLog}
%attr(755,root,root) %{_libdir}/libportaudiocpp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libportaudiocpp.so.0

%files c++-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libportaudiocpp.so
%{_includedir}/portaudiocpp
%{_pkgconfigdir}/portaudiocpp.pc

%if %{with static_libs}
%files c++-static
%defattr(644,root,root,755)
%{_libdir}/libportaudiocpp.a
%endif
