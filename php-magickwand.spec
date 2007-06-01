%define modname magickwand
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A56_%{modname}.ini

Summary:	This module enables PHP access to the ImageMagick MagickWand API
Name:		php-%{modname}
Version:	0.1.9
Release:	%mkrel 6
Group:		Development/PHP
License:	BSD-style
URL:		http://www.magickwand.org/
Source0:	http://www.magickwand.org/download/php/magickwand-%{version}.tar.bz2
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	ImageMagick-devel
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
This module enables PHP access to the ImageMagick MagickWand API.

%prep

%setup -q -n %{modname}

# fix permissions
find . -type f | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make

mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%defattr(-,root,root)
%doc AUTHOR CREDITS ChangeLog LICENSE README TODO
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


