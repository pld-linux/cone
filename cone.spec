Summary:	CONE - Console Newsreader and Emailer
Summary(pl):	CONE - tekstowy klient poczty i czytnik newsów
Name:		cone
Version:	0.60
Release:	1
License:	GPL
Group:		Applications/Mail
Source0:	http://dl.sourceforge.net/courier/%{name}-%{version}.tar.bz2
# Source0-md5:	b2ae0cb3808e5485d566474c8bf251f9
URL:		http://www.courier-mta.org/cone/
BuildRequires:	aspell-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	fam-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	openssl-tools-perl
BuildRequires:	perl-base
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CONE is a simple, text-based E-mail reader and writer, and a simple
newsreader.

%description -l pl
CONE jest prostym, tekstowym klientem pocztowym, a tak¿e prostym
czytnikiem newsów.

%package devel
Summary:	Header files for LibMAIL
Summary(pl):	Pliki nag³ówkowe LibMAIL
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description devel
This package includes the header files for developing applications
using LibMAIL - a high level, C++ OO library for mail clients.

%description devel -l pl
Ten pakiet zawiera pliki nag³ówkowe do tworzenia aplikacji z u¿yciem
LibMAIL - wysokopoziomowej, zorientowanej obiektowo biblioteki C++ dla
klientów pocztowych.

%package static
Summary:	Static LibMAIL library
Summary(pl):	Biblioteka statyczna LibMAIL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static library for developing application using
LibMAIL - a high level, C++ OO library for mail clients.

%description static -l pl
Ten pakiet zawiera statyczn± bibliotekê do tworzenia aplikacji z
u¿yciem LibMAIL - wysokopoziomowej, zorientowanej obiektowo biblioteki
C++ dla klientów pocztowych.

%package -n leaf
Summary:	Console text file editor
Summary(pl):	Konsolowy edytor plików tekstowych
Group:		Applications/Editors

%description -n leaf
Leaf is a simple console text file editor, with paragraph word-wrapping
and spell checking. Leaf is based on the text editor in the Cone mail
reader and composer.

%description -n leaf -l pl
Leaf jest prostym konsolowym edytorem plików tekstowych. Jest oparty na
edytorze u¿ywanym w czytniku poczty Cone.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%{__automake}

CXXFLAGS="%{rpmcflags} -I%{_includedir}/ncurses"
PATH=$PATH:/usr/%{_lib}/openssl; export PATH
%configure \
	--with-devel \
	SENDMAIL=%{_sbindir}/sendmail

%{__make}

%{__make} check

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# start cone directly
mv -f $RPM_BUILD_ROOT%{_libdir}/cone $RPM_BUILD_ROOT%{_bindir}
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/cone.dist $RPM_BUILD_ROOT%{_sysconfdir}/cone

# move devel docs from datadir
mkdir devel
for file in account-* address.html book.html c2*.html e*.html folder-* \
mail-* mimestruct* native* r11* r8* synchronous.html; do
mv -f $RPM_BUILD_ROOT%{_datadir}/cone/$file devel
done

# leaf doc
mv -f $RPM_BUILD_ROOT%{_datadir}/cone/leaf.html .

# rest *.html will go to primary docs
mkdir docs
mv -f $RPM_BUILD_ROOT%{_datadir}/cone/*.html docs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README NEWS docs/
%config(noreplace)  %verify(not size mtime md5) %{_sysconfdir}/cone
%attr(755,root,root) %{_bindir}/cone
%attr(755,root,root) %{_bindir}/mailtool
%{_datadir}/cone
%{_mandir}/man1/cone*
%{_mandir}/man1/mailtool*

%files devel
%defattr(644,root,root,755)
%doc devel/*
%{_includedir}/libmail
%{_mandir}/man[35]/*

%files static
%defattr(644,root,root,755)
%{_libdir}/libmail.a

%files -n leaf
%defattr(644,root,root,755)
%doc leaf.html
%attr(755,root,root) %{_bindir}/leaf
%{_mandir}/man1/leaf*
