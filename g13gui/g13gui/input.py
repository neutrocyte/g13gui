import gi
import evdev
import threading

from evdev import InputDevice
from evdev import KeyEvent
from evdev import ecodes

gi.require_version('Gtk', '3.0')
from gi.repository import GObject, GLib


class InputReader(GObject.Object):
    INPUT_PATH = '/dev/input'

    def __init__(self):
        GObject.Object.__init__(self)

        self._capturing = False
        self._watches = []
        self._keyStates = {}

    def capture(self):
        if self._capturing:
            return False

        self._capturing = True

        self._keyStates = {}

        devices = [InputDevice(path) for path in evdev.list_devices()]
        self._keyboards = [dev for dev in devices
                           if ecodes.EV_KEY in dev.capabilities()]
        self._keyboards = {dev.fd: dev for dev in self._keyboards}
        self._watches = []
        for fd, kbd in self._keyboards.items():
            watch = GLib.io_add_watch(fd,
                                      GLib.PRIORITY_HIGH,
                                      GLib.IO_IN,
                                      self.handleEvent)
            self._watches.append(watch)

        return False

    def stop(self):
        if not self._capturing:
            return False

        for i in self._watches:
            GLib.source_remove(i)

        for fd, kbd in self._keyboards.items():
            del kbd
            del fd

        self._keyboards = None
        self._watches = []
        self._keyStates = {}
        self._capturing = False

        return False

    def handleEvent(self, fd, condition, *args):
        for event in self._keyboards[fd].read():
            if event.type != ecodes.EV_KEY:
                continue

            event = KeyEvent(event)
            if 'BTN_MOUSE' in event.keycode:
                continue

            keyCode = event.scancode
            keyDown = event.keystate in (
                event.key_down, event.key_hold)
            lastKeyState = self._keyStates.get(keyCode, False)

            if keyDown and not lastKeyState:
                self.emit('evdev-key-pressed',
                          keyCode, event.event.timestamp())
            elif not keyDown and lastKeyState:
                self.emit('evdev-key-released',
                          keyCode, event.event.timestamp())

            self._keyStates[keyCode] = keyDown

        return True

    @GObject.Signal(name='evdev-key-released', arg_types=[int, float])
    def keyReleased(self, keyCode, time):
        pass

    @GObject.Signal(name='evdev-key-pressed', arg_types=[int, float])
    def keyPressed(self, keyCode, time):
        pass
