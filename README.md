The G13 Configurator
====================

## What is this?

This is a stand-alone companion application and user space driver for
configuring a Logitech G13 game board. The original code was based upon another
driver originally written by ecraven, and available at
https://github.com/jtgans/g13, but this codebase was modernized, cleaned up
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
