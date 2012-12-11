%define modname magickwand
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A56_%{modname}.ini

Summary:	This module enables PHP access to the ImageMagick MagickWand API
Name:		php-%{modname}
Version:	1.0.9
Release:	%mkrel 2
Group:		Development/PHP
License:	BSD-style
URL:		http://www.magickwand.org/
Source0:	http://www.magickwand.org/download/php/MagickWandForPHP-%{version}.tar.gz
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	imagemagick-devel >= 6.3.5
BuildRequires:	file
BuildRequires:	libxt-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This module enables PHP access to the ImageMagick MagickWand API.

%prep

%setup -q -n MagickWandForPHP-%{version}

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%defattr(-,root,root)
%doc AUTHOR CREDITS ChangeLog LICENSE README TODO
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.9-2mdv2012.0
+ Revision: 795471
- rebuild for php-5.4.x

* Tue Apr 10 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.9-1
+ Revision: 790154
- 1.0.9

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-16
+ Revision: 761263
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-15
+ Revision: 696439
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-14
+ Revision: 695414
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-13
+ Revision: 646656
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-12mdv2011.0
+ Revision: 629818
- rebuilt for php-5.3.5

* Tue Jan 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-11mdv2011.0
+ Revision: 628553
- fix deps (libxt-devel)
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-10mdv2011.0
+ Revision: 600503
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-9mdv2011.0
+ Revision: 588841
- rebuild

* Thu Jul 15 2010 Funda Wang <fwang@mandriva.org> 1.0.8-8mdv2011.0
+ Revision: 553491
- rebuild for new imagemagick

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-7mdv2010.1
+ Revision: 514567
- rebuilt for php-5.3.2

* Thu Jan 14 2010 Funda Wang <fwang@mandriva.org> 1.0.8-6mdv2010.1
+ Revision: 491457
- rebuild for new imagemagick

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-5mdv2010.1
+ Revision: 485400
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-4mdv2010.1
+ Revision: 468183
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-3mdv2010.0
+ Revision: 451286
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1.0.8-2mdv2010.0
+ Revision: 397547
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-1mdv2010.0
+ Revision: 376962
- 1.0.8

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.7-3mdv2009.1
+ Revision: 346511
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.7-2mdv2009.1
+ Revision: 341773
- rebuilt against php-5.2.9RC2

* Sun Feb 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.7-1mdv2009.1
+ Revision: 336170
- 1.0.7
- drop the imagemagick-6.3.8.5 patch, it's fixed upstream

* Thu Jan 29 2009 Götz Waschk <waschk@mandriva.org> 1.0.6-5mdv2009.1
+ Revision: 335085
- rebuild for new libmagick

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-4mdv2009.1
+ Revision: 321866
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-3mdv2009.1
+ Revision: 310283
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-2mdv2009.0
+ Revision: 238408
- rebuild

* Mon Feb 11 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-1mdv2008.1
+ Revision: 165412
- 1.0.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.5-2mdv2008.1
+ Revision: 162101
- rebuild

* Tue Jan 08 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.5-1mdv2008.1
+ Revision: 146508
- rebuilt against new imagemagick libs (6.3.7)
- fix deps
- 1.0.5
- restart apache if needed

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.9-9mdv2008.0
+ Revision: 77554
- rebuilt against php-5.2.4

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.9-8mdv2008.0
+ Revision: 39505
- use distro conditional -fstack-protector
- fix deps

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.9-6mdv2008.0
+ Revision: 33843
- rebuilt against new upstream version (5.2.3)

* Mon May 07 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 0.1.9-5mdv2008.0
+ Revision: 24888
- Rebuild with new libjasper.

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.9-4mdv2008.0
+ Revision: 21338
- rebuilt against new upstream version (5.2.2)


* Wed Mar 21 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.9-3mdv2007.1
+ Revision: 147246
- rebuild

* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.9-2mdv2007.1
+ Revision: 117594
- rebuilt against new upstream version (5.2.1)

* Sat Jan 27 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.9-1mdv2007.1
+ Revision: 114357
- Import php-magickwand

* Sat Jan 27 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.9-1mdv2007.1
- initial Mandriva package

