#
# Conditional build:
%bcond_without	tests	# "make check"
%bcond_with	gnutls	# GnuTLS instead of OpenSSL
%bcond_with	socks	# (Courier) Socks support

Summary:	CONE - Console Newsreader and Emailer
Summary(pl.UTF-8):	CONE - tekstowy klient poczty i czytnik newsów
Name:		cone
Version:	1.5
Release:	2
License:	GPL v3 with OpenSSL exception
Group:		Applications/Mail
Source0:	https://downloads.sourceforge.net/courier/%{name}-%{version}.tar.bz2
# Source0-md5:	a67ea05b272b17f4333ec648a9f7c809
Patch0:		%{name}-maildir.patch
Patch1:		%{name}-curses.patch
URL:		http://www.courier-mta.org/cone/
BuildRequires:	aspell-devel
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
%{?with_socks:BuildRequires:	courier-sox-devel}
BuildRequires:	courier-unicode-devel >= 2.1
BuildRequires:	gettext-tools
# or gnupg2 --with-gpg2, will use the same at runtime
BuildRequires:	gnupg
%{?with_gnutls:BuildRequires:	gnutls-devel >= 3.0}
%{?with_gnutls:BuildRequires:	libgcrypt-devel}
%{?with_gnutls:BuildRequires:	libgpg-error-devel}
BuildRequires:	libidn-devel >= 0.0.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	ncurses-devel >= 5
BuildRequires:	openldap-devel
%{!?with_gnutls:BuildRequires:	openssl-devel >= 0.9.7d}
BuildRequires:	pcre2-8-devel
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	procps
BuildRequires:	sysconftool
BuildRequires:	zlib-devel
Requires:	ca-certificates
Suggests:	gnupg
Conflicts:	courier-imap < 5
Conflicts:	courier-imapd < 1
Conflicts:	maildrop < 3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CONE is a simple, text-based E-mail reader and writer, and a simple
newsreader.

%description -l pl.UTF-8
CONE jest prostym, tekstowym klientem pocztowym, a także prostym
czytnikiem newsów.

%package devel
Summary:	Header files and static LibMAIL library
Summary(pl.UTF-8):	Pliki nagłówkowe i biblioteka statyczna LibMAIL
Group:		Development/Libraries
Requires:	courier-unicode-devel >= 2.0
%{?with_gnutls:Requires:	gnutls-devel >= 3.0}
Requires:	libidn-devel >= 0.0.0
Requires:	libstdc++-devel
%{!?with_gnutls:Requires:	openssl-devel >= 0.9.7d}
Obsoletes:	cone-static < 0.96

%description devel
This package includes the header files and static library for
developing applications using LibMAIL - a high level, C++ OO library
for mail clients.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe i bibliotekę statyczną do
tworzenia aplikacji z użyciem LibMAIL - wysokopoziomowej,
zorientowanej obiektowo biblioteki C++ dla klientów pocztowych.

%package -n leaf
Summary:	Console text file editor
Summary(pl.UTF-8):	Konsolowy edytor plików tekstowych
Group:		Applications/Editors

%description -n leaf
Leaf is a simple console text file editor, with paragraph
word-wrapping and spell checking. Leaf is based on the text editor in
the Cone mail reader and composer.

%description -n leaf -l pl.UTF-8
Leaf jest prostym konsolowym edytorem plików tekstowych, z zawijaniem
wierszy w akapitach i sprawdzaniem pisowni. Jest oparty na edytorze
używanym w czytniku poczty Cone.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
for d in $(sed -ne 's/.*AC_CONFIG_SUBDIRS(\([^)]*\))/\1/p' configure.ac) . ; do
	if [ -d "$d" ]; then
		cd $d
		%{__aclocal}
		%{__autoconf}
		if grep -q AC_CONFIG_HEADER configure.ac ; then
			%{__autoheader}
		fi
		%{__automake}
		cd -
	fi
done

%configure \
	SENDMAIL=/usr/lib/sendmail \
	--with-certdb=%{_sysconfdir}/certs/ca-certificates.crt \
	--with-devel \
	%{?with_gnutls:--with-gnutls} \
	--with-notice=unicode

%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/cone.dist $RPM_BUILD_ROOT%{_sysconfdir}/cone

# move docs to more specific location
install -d $RPM_BUILD_ROOT%{_docdir}/%{name}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/cone/{*.html,manpage.css} $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun -- %{name} < 1
%banner -e cone-unicode <<EOF
WARNING: you have to convert any existing maildirs to Unicode naming scheme.
See INSTALL file for details.
EOF

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cone
%attr(755,root,root) %{_bindir}/cone
%attr(755,root,root) %{_bindir}/mailtool
%attr(755,root,root) %{_libexecdir}/cone
%{_datadir}/cone
%{_mandir}/man1/cone.1*
%{_mandir}/man1/mailtool.1*
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/FAQ.html
%{_docdir}/%{name}/INSTALL.html
%{_docdir}/%{name}/README.html
%{_docdir}/%{name}/add.html
%{_docdir}/%{name}/attributes.html
%{_docdir}/%{name}/bk01-toc.html
%{_docdir}/%{name}/cone*.html
%{_docdir}/%{name}/conn.html
%{_docdir}/%{name}/index.html
%{_docdir}/%{name}/maillist.html
%{_docdir}/%{name}/mailtool.html
%{_docdir}/%{name}/manpage.css
%{_docdir}/%{name}/moredocs.html
%{_docdir}/%{name}/search.html
%{_docdir}/%{name}/smap*.html
%{_docdir}/%{name}/store.html

%files devel
%defattr(644,root,root,755)
%{_libdir}/libmail.a
%{_libdir}/libmail.la
%{_includedir}/libmail
%{_mandir}/man3/mail::*.3x*
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/account-*.html
%{_docdir}/%{name}/address.html
%{_docdir}/%{name}/cppnamespace.html
%{_docdir}/%{name}/emailaddress.html
%{_docdir}/%{name}/envelope.html
%{_docdir}/%{name}/folder-*.html
%{_docdir}/%{name}/header-*.html
%{_docdir}/%{name}/libmail*.html
%{_docdir}/%{name}/mail-*.html
%{_docdir}/%{name}/mimestruct.html
%{_docdir}/%{name}/misc.html
%{_docdir}/%{name}/native.html
%{_docdir}/%{name}/synchronous.html

%files -n leaf
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/leaf
%{_mandir}/man1/leaf.1*
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/leaf.html
