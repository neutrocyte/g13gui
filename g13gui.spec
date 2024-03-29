Name:       g13gui
Version:    1
Release:    1
Summary:    A user-space driver and GUI configurator for the Logitech G13
License:    BSD
URL:        https://github.com/jtgans/g13gui
BuildRequires: meson

%description
This is the companion application to the Logitech G13 gameboard, and provides
both configuration tooling, applet hosting, and also a user space driver to
handle translation of keypresses to real Linux input events by way of uinput.

%meson

%prep


%build
%meson
%meson_build

%install
%meson_install

%check

