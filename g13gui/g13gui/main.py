#!/usr/bin/python

import queue
import gi

import g13gui.model as model
import g13gui.ui as ui

from g13gui.g13d import G13DWorker

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject


VERSION = '0.1.0'


if __name__ == '__main__':
    prefs = model.Preferences()
    queue = queue.Queue()

    win = ui.MainWindow(queue, prefs)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()

    worker = G13DWorker(queue, win)
    worker.start()

    Gtk.main()
