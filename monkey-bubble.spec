%define name monkey-bubble
%define version 0.4.0
%define release %mkrel 1

Summary: GNOME clone of the game Bust'a'Move
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://home.gna.org/monkeybubble/downloads/%{name}-%{version}.tar.bz2
Patch3: monkey-bubble-0.3.22-no-werror.patch.bz2
License: GPL
Group: Games/Arcade
Url: http://home.gna.org/monkeybubble/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: gstreamer0.10-plugins-good
BuildRequires: libgnomeui2-devel
BuildRequires: libglade2.0-devel
BuildRequires: libgstreamer-plugins-base-devel
BuildRequires: librsvg-devel
BuildRequires: scrollkeeper
BuildRequires: perl-XML-Parser
BuildRequires: ImageMagick
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
%patch3 -p1
autoconf

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std install_sh=`pwd`/install-sh
%find_lang %name --with-gnome
for omf in %buildroot%_datadir/omf/%name/%name-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/%name-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name.lang
done
mkdir -p $RPM_BUILD_ROOT/%{_menudir}
cat << EOF > $RPM_BUILD_ROOT/%{_menudir}/%{name}
?package(%{name}):command="%name" icon="%{name}.png" \
  needs="X11" section="More Applications/Games/Arcade" title="Monkey Bubble" \
  longtitle="Monkey Bubble Arcade Game" startup_notify="true" xdg="true"
EOF
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
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/%name.schemas > /dev/null


%post
%update_menus
%update_scrollkeeper
%post_install_gconf_schemas %name

%preun
%preun_uninstall_gconf_schemas %name 

%postun
%clean_menus
%clean_scrollkeeper

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
%_menudir/%name
