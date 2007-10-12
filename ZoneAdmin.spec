Summary:	A Web-based administration interface for powerDNS
Name:		ZoneAdmin
Version:	0.2
Release:	0.1
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/zoneadmin/%{name}-%{version}-beta1.tar.gz
# Source0-md5:	a848e14d947d41734d8a23d72d0196da
Patch0:		%{name}-smarty.patch
URL:		http://open.megabit.net/index.php?section=pro_home&project=ZoneAdmin
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	Smarty >= 2.6.18-2
Requires:	webapps
Requires:	webserver(php)
%if %{with trigger}
Requires(triggerpostun):	sed >= 4.0
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_smartyplugindir	/usr/share/php/Smarty/plugins
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_zavar		/var/lib/%{name}
%define		_appdir		%{_datadir}/%{_webapp}

%description
ZoneAdmin is a Web interface for the powerDNS name server using the
MySQL backend. It allows you to manage existing zones and add, remove,
and alter new ones, supports on-the-fly input validation, and allows
comments per zone and per record. Furthermore, it keeps a detailed
history of changes and allows you to temporary enable or disable zones
without having to remove them completely. New zones can use templates
that contain predefined records. It is designed to be used with one of
Apache's authentication methods.

%prep
%setup -q -n %{name}-%{version}-beta1
%patch0 -p1

cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_smartyplugindir},%{_zavar}/templates_c,%{_appdir}}

install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install *.php	$RPM_BUILD_ROOT%{_appdir}
cp -a {contrib,img,includes,lang,tpl}	$RPM_BUILD_ROOT%{_appdir}
cp -a includes/smarty/libs/plugins/*	$RPM_BUILD_ROOT%{_smartyplugindir}
mv $RPM_BUILD_ROOT%{_appdir}/includes/config.php.dist $RPM_BUILD_ROOT%{_sysconfdir}/config.php
ln -s %{_sysconfdir}/config.php		$RPM_BUILD_ROOT%{_appdir}/includes/config.php

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(660,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%{_appdir}/*.php
%dir %{_appdir}/contrib
%{_appdir}/contrib/*.php
%{_appdir}/contrib/*.sql
%dir %{_appdir}/img
%{_appdir}/img/*.gif
%{_appdir}/img/*.png
%dir %{_appdir}/includes
%{_appdir}/includes/*.php
%dir %{_appdir}/includes/smarty/libs/
%{_appdir}/includes/smarty/libs/*.php
%{_appdir}/includes/smarty/libs/*.tpl
%dir %{_appdir}/includes/smarty/libs/internals
%{_appdir}/includes/smarty/libs/internals/*.php
#%dir %{_appdir}/includes/smarty/libs/plugins
#%{_appdir}/includes/smarty/libs/plugins/*.php
#%dir %{_appdir}/includes/smarty_plugins
#%{_appdir}/includes/smarty_plugins/*.php
%dir %{_appdir}/lang
%{_appdir}/lang/*.conf
%dir %{_appdir}/tpl/Boxes
%{_appdir}/tpl/Boxes/*.css
%{_appdir}/tpl/Boxes/*.js
%{_appdir}/tpl/Boxes/*.tpl
%dir %{_appdir}/tpl/Boxes/img
%{_appdir}/tpl/Boxes/img/*.jpg
%{_appdir}/tpl/Boxes/img/*.gif
%{_smartyplugindir}/*
%dir %{_zavar}
%attr(770,root,http) %{_zavar}/templates_c
