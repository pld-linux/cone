#
# TODO:
#	- pl description
#	- maybe split leaf editor ??
#	- look at html files
#
Summary:	CONE mail reader
Summary(pl):	Czytnik poczty
Name:		cone
Version:	0.60
Release:	0.1
License:	GPL
Group:		Applications/Mail
Source0:	http://dl.sourceforge.net/sourceforge/courier/%{name}-%{version}.tar.bz2
# Source0-md5:	b2ae0cb3808e5485d566474c8bf251f9
URL:		http://www.courier-mta.org/cone
BuildRequires:	aspell-devel
BuildRequires:	autoconf
BuildRequires:	fam-devel
BuildRequires:	gcc-c++
BuildRequires:	ncurses-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	openssl-devel
BuildRequires:	perl
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CONE is a simple, text-based E-mail reader and writer.

%description -l pl
CONE jest prostym, tekstowym klientem pocztowym.

%package	devel
Group:		Development/Languages
Summary:	Header files for LibMAIL
Summary(pl):	Pliki nag³ówkowe LibMAIL
Requires:	%{name} = %{version}-%{release}

%description devel
This package includes the header files for developing application using
LibMAIL - a high level, C++ OO library for mail clients.

%description devel -l pl
pusty

%package	static
Group:		Development/Libraries
Summary:	Static libraries for LibMAIL
Summary(pl):	Biblioteki statyczne LibMAIL
Requires:	%{name} = %{version}-%{release}

%description static
This package includes static files for developing application using
LibMAIL - a high level, C++ OO library for mail clients.

%description static -l pl
pusty

%prep
%setup -q

%build
CXXFLAGS="%{rpmcflags} -I/usr/include/ncurses"
%configure \
    --with-devel

%{__make}

%{__make} check

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# start cone directly
mv -f $RPM_BUILD_ROOT%{_libdir}/cone $RPM_BUILD_ROOT%{_bindir}/
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/cone.dist $RPM_BUILD_ROOT%{_sysconfdir}/cone

# move devel docs from datadir
mkdir devel
for file in account-* address.html book.html c2*.html e*.html folder-* \
mail-* mimestruct* native* r11* r8* synchronous.html; do
mv -f $RPM_BUILD_ROOT%{_datadir}/cone/$file devel
done

# rest *.html will go to primary docs
mkdir docs
mv -f $RPM_BUILD_ROOT%{_datadir}/cone/*.html docs

# install missing files
install libmail/mailtool $RPM_BUILD_ROOT%{_bindir}/mailtool
install help.txt $RPM_BUILD_ROOT%{_datadir}/cone/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ABOUT-NLS ChangeLog README NEWS AUTHORS docs/
%attr(0644,root,root) %config(noreplace)  %verify(not size mtime md5) %{_sysconfdir}/cone
%attr(0755,root,root) %{_bindir}/cone
%attr(0755,root,root) %{_bindir}/leaf
%attr(0755,root,root) %{_bindir}/mailtool
%{_datadir}/cone
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%doc devel/
%{_mandir}/man[35]/*
%{_includedir}/libmail

%files static
%defattr(644,root,root,755)
%{_libdir}/libmail.a
