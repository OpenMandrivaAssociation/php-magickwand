%define modname magickwand
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A56_%{modname}.ini
%define upstream_version 1.0.9-2
%define base_version 1.0.9

Summary:	This module enables PHP access to the ImageMagick MagickWand API

Name:		php-%{modname}
Version:	1.0.9.2
Release:	4
Group:		Development/PHP
License:	BSD-style
URL:		https://www.magickwand.org/
Source0:	http://www.magickwand.org/download/php/MagickWandForPHP-%{upstream_version}.tar.gz
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	imagemagick-devel >= 6.3.5
BuildRequires:	file
BuildRequires:	libxt-devel

%description
This module enables PHP access to the ImageMagick MagickWand API.

%prep

%setup -q -n MagickWandForPHP-%{base_version}

# fix permissions
find . -type f | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# lib64 fixes
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make

mv modules/*.so .

%install
install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun
if [ "$1" = "0" ]; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%clean
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%doc AUTHOR CREDITS ChangeLog LICENSE README TODO
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


