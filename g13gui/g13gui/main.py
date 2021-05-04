#!/usr/bin/python

import gi

import g13gui.ui as ui
from g13gui.model.prefsstore import PreferencesStore
from g13gui.g13.manager import Manager

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject


if __name__ == '__main__':
    Gdk.threads_init()

    prefs = PreferencesStore.getPrefs()
    manager = Manager(prefs)
    manager.start()

    indicator = ui.AppIndicator(prefs)

    Gtk.main()
