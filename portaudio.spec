#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
%bcond_without	apidocs		# documentation generated with doxygen
#
Summary:	Free, cross platform, open-source, audio I/O library
Summary(pl.UTF-8):	Darmowa, międzyplatformowa i otwarta biblioteka I/O audio
Name:		portaudio
Version:	19
%define	snap	20071207
Release:	1.%{snap}.1
License:	LGPL-like
Group:		Libraries
Source0:	http://www.portaudio.com/archives/pa_stable_v%{version}_%{snap}.tar.gz
# Source0-md5:	d2943e4469834b25afe62cc51adc025f
Patch0:		%{name}-ac.patch
URL:		http://www.portaudio.com/
BuildRequires:	alsa-lib-devel >= 0.9
BuildRequires:	autoconf >= 2.13
BuildRequires:	automake
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	pkgconfig
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

%description apidocs
Documentation for portaudio API in HTML format generated from portaudio
sources by doxygen.

%description apidocs -l pl.UTF-8
Dokumentacja API portaudio w formacie HTML generowane ze
źrodeł portaudio przez doxygen.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
cp -f /usr/share/automake/config.sub .
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	--enable-static=%{?with_static_libs:yes}%{!?with_static_libs:no}

%{__make}
%{?with_apidocs:/usr/bin/doxygen}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.txt LICENSE.txt
%attr(755,root,root) %{_libdir}/libportaudio.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libportaudio.so.2

%files devel
%defattr(644,root,root,755)
#%doc doc/html/* ???
%attr(755,root,root) %{_libdir}/libportaudio.so
%{_libdir}/libportaudio.la
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
