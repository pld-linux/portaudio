Summary:	Free, cross platform, open-source, audio I/O library
Summary(pl):	Darmowa, miêdzyplatformowa i otwarta biblioteka I/O audio
Name:		portaudio
Version:	19
Release:	1
License:	LGPL-like
Group:		Libraries
Source0:	http://www.portaudio.com/archives/pa_snapshot_v%{version}.tar.gz
# Source0-md5:	ee93573d41f2867bf319addddd4eb6bf
BuildRequires:	alsa-lib-devel >= 0.9
BuildRequires:	autoconf >= 2.13
BuildRequires:	automake
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
URL:		http://www.portaudio.com/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PortAudio is a free, cross platform, open-source, audio I/O library.
It lets you write simple audio programs in 'C' that will compile and
run on many platforms including Windows, Macintosh (8,9,X), Unix
(OSS), SGI, and BeOS.

%description -l pl
PortAudio to darmowa, miêdzyplatformowa i otwarta biblioteka I/O
audio. Pozwala na pisanie prostych programów w "C", które bêd± siê
kompilowaæ i uruchamiaæ na wielu platformach, w tym Windows, Macintosh
(8,9,X), Unix (OSS), SGI, i BeOS.

%package devel
Summary:	Header files for PortAudio library
Summary(pl):	Pliki nag³ówkowe biblioteki PortAudio
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for PortAudio library.

%description devel -l pl
Pliki nag³ówkowe biblioteki PortAudio.

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

sed -i -e '/^CFLAGS="-g -O2 -Wall"/d' configure.in

%build
%{__aclocal}
%{__autoconf}
%configure
%{__make} \
	SHARED_FLAGS="-shared -Wl,-soname=libportaudio.so.0"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}

%{__make} install \
	PREFIX=$RPM_BUILD_ROOT/usr

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.txt LICENSE.txt
%attr(755,root,root) %{_libdir}/libportaudio.so.*.*

%files devel
%defattr(644,root,root,755)
%doc docs/*
%attr(755,root,root) %{_libdir}/libportaudio.so
%{_includedir}/portaudio.h

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
