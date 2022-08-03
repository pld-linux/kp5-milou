#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	5.25.4
%define		qtver		5.15.2
%define		kpname		milou
Summary:	A dedicated search application built on top of Baloo
Name:		kp5-%{kpname}
Version:	5.25.4
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	7db4206e533f247b878241158f946552
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-extra-cmake-modules >= 1.4.0
BuildRequires:	kf5-kdeclarative-devel
BuildRequires:	kf5-ki18n-devel
BuildRequires:	kf5-krunner-devel
BuildRequires:	kf5-kservice-devel
BuildRequires:	kf5-plasma-framework-devel
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A dedicated search application built on top of Baloo.

%prep
%setup -q -n %{kpname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	..
%ninja_build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%ghost %{_libdir}/libmilou.so.5
%attr(755,root,root) %{_libdir}/libmilou.so.*.*.*
%{_libdir}/qt5/qml/org/kde/milou
%{_datadir}/plasma/plasmoids/org.kde.milou
%{_datadir}/metainfo/org.kde.milou.appdata.xml
%{_datadir}/kservices5/plasma-applet-org.kde.milou.desktop
