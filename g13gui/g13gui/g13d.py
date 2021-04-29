#!/usr/bin/python3

import gi
import os
import os.path
import threading
import time
import traceback
import xdg.BaseDirectory as basedir
import json

from g13gui.model import PreferencesStore
from g13gui.common import PROFILES_CONFIG_PATH
from g13gui.common import VERSION

gi.require_version('Gtk', '3.0')
from gi.repository import GObject


class UploadTask():
    def __init__(self, commands):
        self._commands = str.encode(commands)

    def run(self, outfp, infp, callback):
        bytes_written = 0
        while bytes_written < len(self._commands):
            result = os.write(outfp, self._commands[bytes_written:])
            if result > 0:
                bytes_written = result + bytes_written
            callback(bytes_written / len(self._commands))
        callback(1.0)


class SaveTask():
    def __init__(self, prefs):
        self._prefs = prefs

    def run(self, outfp, infp, callback):
        PreferencesStore.storePrefs(self._prefs)


G13D_IN_FIFO = "/run/g13d/in"
G13D_OUT_FIFO = "/run/g13d/out"


class G13DWorker(threading.Thread):
    def __init__(self, q, window):
        threading.Thread.__init__(self, daemon=True)
        self._mainWindow = window
        self._queue = q
        self._connected = False

    def _connect(self):
        try:
            self._outfp = os.open(G13D_IN_FIFO, os.O_WRONLY)
            self._infp = os.open(G13D_OUT_FIFO, os.O_RDONLY)

        except FileNotFoundError:
            self._outfp = None
            self._infp = None
            self._connected = False
            self._mainWindow.emit("daemon-connection-changed", False)
            time.sleep(10)

        except Exception as err:
            self._outfp = None
            self._infp = None
            self._connected = False
            print("Unknown exception occurred: %s %s" % (type(err), err))
            self._mainWindow.emit("daemon-connection-changed", False)
            time.sleep(10)

        else:
            self._mainWindow.emit("daemon-connection-changed", True)
            self._connected = True

    def run(self):
        while True:
            while not self._connected:
                self._connect()

            item = self._queue.get()

            try:
                item.run(self._outfp, self._infp, self.callback)
            except BrokenPipeError as err:
                print("g13d connection broken: %s" % (err))
                self._connected = False
            except Exception as err:
                traceback.print_exc()
            finally:
                self._queue.task_done()

    def callback(self, percentage):
        self._mainWindow.emit("uploading", percentage)

    def getQueue(self):
        return self._queue
