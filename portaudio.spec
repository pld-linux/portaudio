Summary:	Free, cross platform, open-source, audio I/O library
Summary(pl):	Darmowa, mi�dzyplatformowa i otwarta biblioteka I/O audio
Name:		portaudio
Version:	18
Release:	1
License:	LGPL-like
Group:		Libraries
Source0:	http://www.portaudio.com/archives/%{name}_v%{version}_1.zip
# Source0-md5:	ce66a732d263fde2b5ad2262ef37a691
URL:		http://www.portaudio.com/
BuildRequires:	unzip
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

%description devel
Header files for PortAudio library.

%description devel -l pl
Pliki nag��wkowe biblioteki PortAudio.

%prep
%setup -q -n %{name}_v%{version}_1

%build
mv Makefile.linux Makefile
%{__make} sharedlib \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}

install pa_unix_oss/libportaudio.so $RPM_BUILD_ROOT%{_libdir}
install pa_common/portaudio.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.txt LICENSE.txt
%attr(755,root,root) %{_libdir}/libportaudio.so

%files devel
%defattr(644,root,root,755)
%doc docs/*
%{_includedir}/portaudio.h
