Name:           leveldb
Version:        1.20
Release:        1%{?dist}
Summary:        A fast and lightweight key/value database library by Google
License:        BSD
URL:            https://github.com/google/leveldb
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# available in https://github.com/fusesource/leveldbjni/blob/leveldb.patch
Patch0001:      0001-Allow-leveldbjni-build.patch
# https://github.com/fusesource/leveldbjni/issues/34
# https://code.google.com/p/leveldb/issues/detail?id=184
# Add DB::SuspendCompactions() and DB:: ResumeCompactions() methods
Patch0002:      0002-Added-a-DB-SuspendCompations-and-DB-ResumeCompaction.patch
# Cherry-picked from Basho's fork
Patch0003:      0003-allow-Get-calls-to-avoid-copies-into-std-string.patch
# https://groups.google.com/d/topic/leveldb/SbVPvl4j4vU/discussion
Patch0004:      0004-bloom_test-failure-on-big-endian-archs.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  snappy-devel

%description
LevelDB is a fast key-value storage library written at Google that provides an
ordered mapping from string keys to string values.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -p1
cat > %{name}.pc << EOF
prefix=%{_prefix}
exec_prefix=${prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: %{name}
Description: %{summary}
Version: %{version}
Libs: -l%{name}
EOF

%global configure() {                  \
  export OPT="-DNDEBUG"                \
  export CFLAGS="%{optflags}"          \
  export CXXFLAGS="%{optflags}"        \
  export LDFLAGS="%{__global_ldflags}" \
}

%build
%configure
# Compilation fails randomly when run in parallel
%make_build -j1

%install
mkdir -p %{buildroot}{%{_libdir}/pkgconfig,%{_includedir}}
cp -a out-shared/lib%{name}.so* %{buildroot}%{_libdir}/
cp -a include/%{name}/ %{buildroot}%{_includedir}/
cp -a %{name}.pc %{buildroot}%{_libdir}/pkgconfig/

%check
%configure
make -j1 check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc AUTHORS README.md NEWS
%{_libdir}/lib%{name}.so.*

%files devel
%doc doc/ CONTRIBUTING.md TODO
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Mon Oct 23 2017 Stephen Gallagher <sgallagh@redhat.com> - 1.20-1
- Update to 1.20
- Disable parallel make invocation to prevent build failures

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Aug 07 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.18-1
- Update to 1.18 (RHBZ #1306611)
- Cleanups and fixes in spec

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Tomas Hozza <thozza@redhat.com> - 1.12.0-9
- rebuild with newer gcc to resolve linking issues with Ceph

* Sun Mar  1 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.0-8
- F-23: rebuild for gcc5 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 25 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.12.0-5
- Don't build with assertions

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 10 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.12.0-3
- Backported Basho's patch (see rhbz#982980)

* Mon Jul 01 2013 gil cattaneo <puntogil@libero.it> 1.12.0-2
- add SuspendCompactions and ResumeCompactions methods for allow leveldbjni build

* Sat Jun 29 2013 gil cattaneo <puntogil@libero.it> - 1.12.0-1
- update to 1.12.0

* Wed Feb 27 2013 gil cattaneo <puntogil@libero.it> - 1.9.0-1
- update to 1.9.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Feb 07 2013 Karsten Hopp <karsten@redhat.com> 1.7.0-5
- temporarily ignore result of self checks on PPC* (rhbz #908800)

* Thu Nov 29 2012 gil cattaneo <puntogil@libero.it> - 1.7.0-4
- Applied patch for allow leveldbjni build

* Sat Oct 27 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.7.0-3
- Dirty workarounds for failed tests on ARM

* Sat Oct 27 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.7.0-2
- Restored patch no.2

* Sat Oct 27 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.7.0-1
- Ver. 1.7.0 (API/ABI compatible bugfix release)

* Tue Aug 21 2012 Dan Horák <dan[at]danny.cz> - 1.5.0-4
- add workaround for big endians eg. s390(x)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.5.0-2
- Cleaned up spec by removing EL5-related stuff
- Added notes about the patches

* Fri Jun 15 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.5.0-1
- Ver. 1.5.0

* Thu May 17 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.4.0-1
- Initial package
