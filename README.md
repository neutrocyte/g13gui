The G13 Configurator
====================

![GUI Screenshot](assets/g13gui.png)

## What is this?

This is a stand-alone companion application and user space driver for
configuring a Logitech G13 game board. The original code was based upon another
driver originally written by ecraven, and available at
https://github.com/ecraven/g13, but this codebase was modernized, cleaned up
and totally rewritten in Python.

Using this tool allows you to:

  - Graphically plan out a keymapping profile
  - Save multiple profiles and switch between them at will
  - Use the LCD with pluggable dbus-based applets to display
    useful information
  - Switch profiles using the LCD

All wrapped up in a glorious Gtk 3.0 + libappindicator interface.

Please note: this is an early version of the application and as such it is still
in heavy development, but the author uses it almost on a daily basis already to
play most of her game library.

## Building

[![Build Status](https://drone.hedron.io/api/badges/jtgans/g13gui/status.svg)](https://drone.hedron.io/jtgans/g13gui)

We have a continuous build running to make packaging, and periodically those
artifacts are brought over as releases on the Github site. The CI is run on
June's personal infrastructure via a gitea mirror, so releases may lag behind
a slight bit. June promises to redouble her efforts. :D

In general, though, g13gui is a python program, so no actual compilation takes
place. All the Makefile and associated infrastructure do is assemble distro
specific packages. If you want to skip the packaging (not recommended), it's
entirely possible to run the program out of the source tree by doing the
following:

```
[user@host g13gui]$ export PYTHONPATH=$PWD
[user@host g13gui]$ bin/g13gui &
[user@host g13gui]$ bin/g13-clock &
[user@host g13gui]$ bin/g13-profiles &
```

Note that you will have to manually install the udev rules file in `etc/` to
your appropriate distro-specific location.

### Building a package

In the major distributions, it should just be possible to run `make` to build
a package for your specific distro. As of this writing, there is support to
build for Debian, Ubuntu, Arch, and Manjaro. Patches are welcome to help improve
availability on other platforms.

#### Debian and Debian derivatives

First, setup your system with build tooling:

```
lupin:~$ sudo apt-get install devscripts python3 build-essential git-buildpackage appstream dh-sequence-python3 meson
```

Now you can build the package:

```
lupin:~/src/g13gui$ make
```

