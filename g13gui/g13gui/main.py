#!/usr/bin/python

import gi
import queue

import g13gui.ui as ui
from g13gui.model.prefsstore import PreferencesStore
from g13gui.g13.manager import Manager

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject


if __name__ == '__main__':
    prefs = PreferencesStore.getPrefs()
    manager = Manager(prefs)
    manager.start()

    queue = queue.Queue()

    win = ui.MainWindow(queue, prefs)
    win.show_all()

    indicator = ui.AppIndicator(prefs, win)

    Gtk.main()
