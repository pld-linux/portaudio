#
# Conditional build:
%bcond_without	static_libs # don't build static libraries
#
Summary:	Free, cross platform, open-source, audio I/O library
Summary(pl):	Darmowa, mi�dzyplatformowa i otwarta biblioteka I/O audio
Name:		portaudio
Version:	19
Release:	1.20060926.1
License:	LGPL-like
Group:		Libraries
Source0:	http://www.portaudio.com/archives/pa_snapshot_v%{version}.tar.gz
# Source0-md5:	e418b70d4df87f269dfc346682c0ce7b
Patch0:		%{name}-ac.patch
URL:		http://www.portaudio.com/
BuildRequires:	alsa-lib-devel >= 0.9
BuildRequires:	autoconf >= 2.13
BuildRequires:	automake
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PortAudio is a free, cross platform, open-source, audio I/O library.
It lets you write simple audio programs in 'C' that will compile and
run on many platforms including Windows, Macintosh (8,9,X), Unix
(OSS), SGI, and BeOS.

%description -l pl
PortAudio to darmowa, mi�dzyplatformowa i otwarta biblioteka I/O
audio. Pozwala na pisanie prostych program�w w "C", kt�re b�d� si�
kompilowa� i uruchamia� na wielu platformach, w tym Windows, Macintosh
(8,9,X), Unix (OSS), SGI, i BeOS.

%package devel
Summary:	Header files for PortAudio library
Summary(pl):	Pliki nag��wkowe biblioteki PortAudio
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
Header files for PortAudio library.

%description devel -l pl
Pliki nag��wkowe biblioteki PortAudio.

%package static
Summary:	Static PortAudio library
Summary(pl):	Statyczna biblioteka PortAudio
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static PortAudio library.

%description static -l pl
Statyczna biblioteka PortAudio.

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

%files devel
%defattr(644,root,root,755)
#%doc docs/*
%attr(755,root,root) %{_libdir}/libportaudio.so
%{_libdir}/libportaudio.la
%{_includedir}/portaudio.h
%{_pkgconfigdir}/portaudio-*.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
