Summary: A debugger which detects memory allocation violations
Name: ElectricFence
Version: 2.2.2
Release: 28%{?dist}
License: GPLv2
Group: Development/Tools
URL: http://perens.com/FreeSoftware/ElectricFence/

# ftp://ftp.perens.com/pub/ElectricFence/beta/ used to be here, but
# the site is inaccessible as of lately
Source: %{name}-%{version}.tar.gz
Patch1: ElectricFence-2.0.5-longjmp.patch
Patch2: ElectricFence-2.1-vaarg.patch
Patch3: ElectricFence-2.2.2-pthread.patch
Patch4: ElectricFence-2.2.2-madvise.patch
Patch5: ElectricFence-mmap-size.patch
Patch6: ElectricFence-2.2.2-banner.patch
Patch7: ElectricFence-2.2.2-ef.patch
Patch8: ElectricFence-2.2.2-posix_memalign.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
ElectricFence is a utility for C programming and
debugging. ElectricFence uses the virtual memory hardware of your
system to detect when software overruns malloc() buffer boundaries,
and/or to detect any accesses of memory released by
free(). ElectricFence will then stop the program on the first
instruction that caused a bounds violation and you can use your
favorite debugger to display the offending statement.

Install ElectricFence if you need a debugger to find malloc()
violations.

%prep
%setup -q
%patch1 -p1 -b .longjmp
%patch2 -p1 -b .vaarg
%patch3 -p1 -b .pthread
%patch4 -p1 -b .madvise
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
make CFLAGS='${RPM_OPT_FLAGS} -DUSE_SEMAPHORE -fpic'

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}{%{_bindir},%{_libdir},%{_mandir}/man3}

make	BIN_INSTALL_DIR=%{buildroot}%{_bindir} \
	LIB_INSTALL_DIR=%{buildroot}%{_libdir} \
	MAN_INSTALL_DIR=%{buildroot}%{_mandir}/man3 \
	install

echo ".so man3/efence.3" > %{buildroot}%{_mandir}/man3/libefence.3

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc README CHANGES COPYING
%{_bindir}/*
%{_libdir}/*.a
%{_libdir}/*.so*
%{_mandir}/*/*

%changelog
* Wed Jun 30 2010 Petr Machata <pmachata@redhat.com> - 2.2.2-28
- Add a patch that implements posix_memalign
- Resolves: #603075

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.2.2-27.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 11 2008 Petr Machata <pmachata@redhat.com> - 2.2.2-25
- Fix ef.sh argument passing
- Resolves: #432286

* Thu Aug 16 2007 Petr Machata <pmachata@redhat.com> - 2.2.2-24
- Fix licesing tag.

* Wed Mar 28 2007 Petr Machata <pmachata@redhat.com> - 2.2.2-23
- Detect for EF_DISABLE_BANNER env. var before printing out the
  banner.  (Patch adapted from Debian repositories.)
- Resolves: #233702

* Fri Mar 16 2007 Petr Machata <pmachata@redhat.com> - 2.2.2-22
- Remove bad cast in ElectricFence mmap (George Beshers)
- Resolves: #232695

* Wed Feb  7 2007 Petr Machata <pmachata@redhat.com> - 2.2.2-21
- Tidy up the specfile per rpmlint comments

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.2.2-20.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.2.2-20.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.2.2-20.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Mar  5 2005 Jakub Jelinek <jakub@redhat.com> 2.2.2-20
- rebuilt with GCC 4

* Sat Oct 16 2004 Jakub Jelinek <jakub@redhat.com> 2.2.2-19
- when EF_PROTECT_FREE=1, instead of munmaping mprotect PROT_NONE
  and madvise MADV_DONTNEED (#107506)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb  3 2003 Jakub Jelinek <jakub@redhat.com>
- never call semaphore routines in between
  __libc_malloc_pthread_startup(true) and
  __libc_malloc_pthread_startup(false) (#83111)
- only use semaphore locking if application or its dependencies
  are linked against -lpthread, don't link libefence.so against
  -lpthread
- run tests as part of the build process

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Jeff Johnson <jbj@redhat.com> 2.2.2-13
- don't include -debuginfo files in package.

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 2.2.2-12
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Thu Nov 16 2000 Tim Powers <timp@redhat.com>
- use -fPIC, not -fpic, also -DUSE_SEMAPHORE to make it thread safe,
  as per bug #20935

* Tue Sep 19 2000 Bill Nottingham <notting@redhat.com>
- use -fpic

* Fri Aug 18 2000 Tim Waugh <twaugh@redhat.com>
- fix efence.3/libefence.3 confusion (#16412).

* Tue Aug 1 2000 Tim Powers <timp@redhat.com>
- added ldconfig stuff to ;post and postun
- added Requires /sbin/ldconfig
* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Jul 05 2000 Preston Brown <pbrown@redhat.com>
- back in main distro
- 2.2.2 version - claimed beta, but no releases in over a year.
- FHS macros

* Fri May 26 2000 Tim Powers <timp@redhat.com>
- moved to Powertools
- fix map page location to be in /usr/share/man

* Tue May 16 2000 Jakub Jelinek <jakub@redhat.com>
- fix build on ia64

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description
- man pages are compressed

* Tue Jan  4 2000 Jeff Johnson <jbj@redhat.com>
- remove ExcludeArch: alpha (#6683).

* Sat Apr 10 1999 Matt Wilson <msw@redhat.com>
- version 2.1

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 13)

* Wed Jan 06 1999 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Fri Aug 21 1998 Jeff Johnson <jbj@redhat.com>
- create efence.3 (problem #830)

* Tue Aug  4 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Jun 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Mon Jun 01 1998 Prospector System <bugs@redhat.com>
- need to use sigsetjmp() and siglongjmp() for proper testing

* Fri May 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- use ExcludeArch instead of Exclude

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc
