#!/usr/bin/python

import sys

from dbus.mainloop.glib import DBusGMainLoop

from g13gui.app import Application


if __name__ == '__main__':
    DBusGMainLoop(set_as_default=True)

    app = Application()
    app.run(sys.argv)
