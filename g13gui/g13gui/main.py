#!/usr/bin/python

import queue
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GObject
from mainwindow import MainWindow
from g13d import G13DWorker


VERSION = '0.1.0'


if __name__ == '__main__':
    queue = queue.Queue()

    win = MainWindow(queue)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()

    worker = G13DWorker(queue, win)
    worker.start()

    Gtk.main()
