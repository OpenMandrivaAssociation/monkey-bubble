%define name monkey-bubble
%define version 0.4.0
%define release %mkrel 4

Summary: GNOME clone of the game Bust'a'Move
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://home.gna.org/monkeybubble/downloads/%{name}-%{version}.tar.bz2
Patch0: monkey-bubble-0.4.0-help.patch
Patch1: monkey-bubble-0.4.0-format-strings.patch
Patch2: monkey-bubble-0.4.0-link.patch
Patch3: monkey-bubble-0.3.22-no-werror.patch
License: LGPLv2+
Group: Games/Arcade
Url: https://home.gna.org/monkeybubble/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: gstreamer0.10-plugins-good
BuildRequires: libgnomeui2-devel
BuildRequires: libglade2.0-devel
BuildRequires: libgstreamer-plugins-base-devel
BuildRequires: librsvg-devel
BuildRequires: scrollkeeper
BuildRequires: gnome-doc-utils
BuildRequires: perl-XML-Parser
BuildRequires: imagemagick
BuildRequires: desktop-file-utils
#gw auto*
BuildRequires: automake1.4
BuildRequires: intltool
BuildRequires: gnome-common
BuildRequires: libtool
BuildRequires: pkgconfig
%description
This is an arcade puzzle game with the goal of making all bubbles in
the game area explode.

You explode bubbles by putting at least 3 of the same colour in
contact. Any bubble that is connected to the top or the sides of the
game area by bubbles you just exploded falls too.

Support for network game with 4 players is included.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p0
sed -i -e 's/-Werror//' src/*/Makefile.*

%build
autoreconf -fi
%configure2_5x --disable-scrollkeeper
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std install_sh=`pwd`/install-sh
%find_lang %name --with-gnome
for omf in %buildroot%_datadir/omf/%name/%name-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/%name-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name.lang
done
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GTK" \
  --add-category="Game;ArcadeGame"\
  --add-category="X-MandrivaLinux-MoreApplications-Games-Arcade" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


mkdir -p %buildroot{%_liconsdir,%_miconsdir}
ln -s %_datadir/pixmaps/%name-icon.png %buildroot%_iconsdir/%name.png
convert -scale 16x16 pixmaps/%name-icon.png %buildroot%_miconsdir/%name.png

%triggerpostun -- %{name} < 0.3.2-3mdk
%post_install_gconf_schemas %name


%if %mdkversion < 200900
%post
%update_menus
%update_scrollkeeper
%post_install_gconf_schemas %name
%endif

%preun
%preun_uninstall_gconf_schemas %name 

%if %mdkversion < 200900
%postun
%clean_menus
%clean_scrollkeeper
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr(-,root,root)
%doc ChangeLog AUTHORS
#README NEWS
%_sysconfdir/gconf/schemas/%name.schemas
%_bindir/%name
%_bindir/monkey-srv
%_datadir/applications/%name.desktop
%_datadir/%name
%_datadir/pixmaps/%name-icon.png
%dir %_datadir/omf/%name
%_datadir/omf/%name/%name-C.omf
%_iconsdir/%name.png
%_miconsdir/%name.png
