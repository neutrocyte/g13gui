#!/usr/bin/python

import gi
import json
import queue

import g13gui.model as model
import g13gui.ui as ui
from g13gui.g13d import G13DWorker
from g13gui.common import PROFILES_CONFIG_PATH

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject


if __name__ == '__main__':
    prefs = model.PreferencesStore.getPrefs()
    queue = queue.Queue()

    win = ui.MainWindow(queue, prefs)
    win.show_all()

    indicator = ui.AppIndicator(prefs, win)

    worker = G13DWorker(queue, win)
    worker.start()

    Gtk.main()
