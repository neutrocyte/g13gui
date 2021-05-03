import threading
import gi
import glob
import asyncio

gi.require_version('Gtk', '3.0')
from gi.repository import GObject

import evdev
from evdev import InputDevice
from evdev import ecodes
from select import select


class InputReader(threading.Thread, GObject.GObject):
    INPUT_PATH = '/dev/input'

    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        GObject.GObject.__init__(self)
        self.reset()

    def reset(self):
        self._isRunning = False
        self._keyStates = {}

    @GObject.Signal(name='evdev-key-released')
    def keyReleased(self, keyCode, time):
        print('key released: %d')

    @GObject.Signal(name='evdev-key-pressed')
    def keyPressed(self, keyCode, time):
        print('key pressed: %d')

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        devices = [InputDevice(path) for path in evdev.list_devices()]
        keyboards = [dev for dev in devices if ecodes.EV_KEY in dev.capabilities()]
        print('Have keyboards: %s' % (keyboards))

        while self._isRunning:
            r, w, x = select(keyboards, [], [])
            print('keyboards listening!')
            for fd in r:
                for event in keyboards[fd].read():
                    if event.type != ecodes.EV_KEY:
                        continue

                    keyCode = event.keycode
                    keyDown = event.keystate == event.key_down
                    lastKeyState = self._keystates.get(keyCode, False)

                    if keyDown and not lastKeyState:
                        self.emit('evdev-key-pressed',
                                  keyCode, event.event.timestamp())
                    elif not keyDown and lastKeyState:
                        self.emit('evdev-key-released',
                                  keyCode, event.event.timestamp())

    def shutdown(self):
        self._isRunning = False
