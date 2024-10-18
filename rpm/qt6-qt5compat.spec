%global qt_version 6.7.2

%global qt_module qt5compat

Summary: Qt6 - Qt 5 Compatibility Libraries
Name:    qt6-qt5compat
Version: 6.7.2
Release: 0%{?dist}

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
%global majmin %(echo %{qt_version} | cut -d. -f1-2)

Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{qt_version}/submodules/%{qt_module}-everywhere-src-%{qt_version}.tar.xz

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: qt6-qtbase-devel >= %{version}
BuildRequires: qt6-qtbase-private-devel
# qt6-qtdeclarative is required for QtGraphicalEffects
BuildRequires: qt6-qtdeclarative-devel
BuildRequires: qt6-qtshadertools-devel
BuildRequires: pkgconfig(xkbcommon)
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: libicu-devel

%description
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
%description devel
%{summary}.

%prep
%autosetup -n %{name}-%{version}/upstream -p1


%build
%cmake_qt6 \
  -DQT_BUILD_EXAMPLES:BOOL=OFF \
  -DQT_INSTALL_EXAMPLES_SOURCES=OFF

%cmake_build


%install
%cmake_install


## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


#%%ldconfig_scriptlets

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSES/*
%{_qt6_libdir}/libQt6Core5Compat.so.6*
%{_qt6_libdir}/qt6/qml/Qt5Compat/GraphicalEffects/*

%files devel
%{_qt6_headerdir}/QtCore5Compat/
%{_qt6_libdir}/libQt6Core5Compat.prl
%{_qt6_libdir}/libQt6Core5Compat.so
%{_qt6_libdir}/cmake/Qt6/FindWrapIconv.cmake
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/*.cmake
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/Qt5CompatTestsConfig.cmake
%dir %{_qt6_libdir}/cmake/Qt6Core5Compat/
%{_qt6_libdir}/cmake/Qt6Core5Compat/*.cmake
%{_qt6_archdatadir}/mkspecs/modules/*.pri
%{_qt6_libdir}/qt6/modules/*.json
%{_qt6_libdir}/qt6/metatypes/qt6*_metatypes.json
%{_qt6_libdir}/pkgconfig/*.pc

