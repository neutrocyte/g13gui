import gi
import dbus
import dbus.service
import dbus.mainloop.glib
import time

from dbus.mainloop.glib import DBusGMainLoop
from dbus.exceptions import DBusException
from dbus.types import ByteArray

from g13gui.applet.loopbackdisplaydevice import LoopbackDisplayDevice
from g13gui.bitwidgets.display import Display
from g13gui.bitwidgets.screen import Screen

gi.require_version('GLib', '2.0')
from gi.repository import GLib


class Buttons(object):
    L1 = 1
    L2 = 2
    L3 = 3
    L4 = 4


class Applet(dbus.service.Object):
    BUS_INTERFACE = 'com.theonelab.g13.Applet'
    BUS_PATH = '/com/theonelab/g13/Applet'

    def __init__(self, name):
        dbus.service.Object.__init__(self, dbus.SessionBus(),
                                     Applet.BUS_PATH)

        self._name = name
        self._dd = LoopbackDisplayDevice()
        self._d = Display(self._dd)
        self._s = Screen(self._d)
        self._s.hide()

        self._registered = False
        self._manager = None

    def register(self):
        try:
            self._manager = self._bus.get_object(
                'com.theonelab.g13.AppletManager',
                '/com/theonelab/g13/AppletManager')
        except DBusException:
            self._manager = None
            return True

        self._manager.Register(self._name)
        self._registered = True
        GLib.timeout_add_seconds(1, self._ping)

        return False

    def _ping(self):
        if self._manager:
            try:
                self._manager.Ping()
            except DBusException as err:
                print('Lost connection with AppletManager: %s' % err)
                self._registered = False
                GLib.timeout_add_seconds(1, self.register)
                return False

        return True

    def run(self):
        self._bus = dbus.SessionBus()

        GLib.timeout_add_seconds(1, self.register)

        loop = GLib.MainLoop()
        loop.run()

    @property
    def name(self):
        return self._name

    @property
    def displayDevice(self):
        return self._dd

    @property
    def display(self):
        return self._d

    @property
    def screen(self):
        return self._s

    def onKeyPressed(self, timestamp, key):
        pass

    def onKeyReleased(self, timestamp, key):
        pass

    def onShown(self, timestamp):
        pass

    def onHidden(self):
        pass

    def onUpdateScreen(self):
        pass

    def maybePresentScreen(self):
        if self.screen.visible and self._manager:
            self.screen.nextFrame()
            frame = self.displayDevice.frame
            frame = ByteArray(frame)
            self._manager.Present(frame, byte_arrays=True)

    @dbus.service.method(BUS_INTERFACE,
                         in_signature='d', out_signature='ay',
                         byte_arrays=True)
    def Present(self, timestamp):
        self.screen.show()
        self.onShown(timestamp)
        self.screen.nextFrame()
        return ByteArray(self.displayDevice.frame)

    @dbus.service.method(BUS_INTERFACE)
    def Unpresent(self):
        self.screen.hide()
        self.onHidden()

    def _setButtonPressed(self, state, button):
        buttonIdx = button - 1
        button = self._s.buttonBar.button(buttonIdx)
        if button:
            button.pressed = state

    @dbus.service.method(BUS_INTERFACE,
                         in_signature='di', out_signature='ay',
                         byte_arrays=True)
    def KeyPressed(self, timestamp, key):
        self.onKeyPressed(timestamp, key)
        self._setButtonPressed(True, key)
        self.onUpdateScreen()
        self.screen.nextFrame()
        return ByteArray(self.displayDevice.frame)

    @dbus.service.method(BUS_INTERFACE,
                         in_signature='di', out_signature='ay',
                         byte_arrays=True)
    def KeyReleased(self, timestamp, key):
        self.onKeyPressed(timestamp, key)
        self._setButtonPressed(False, key)
        self.onUpdateScreen()
        self.screen.nextFrame()
        return ByteArray(self.displayDevice.frame)


def RunApplet(cls, *args, **kwargs):
    DBusGMainLoop(set_as_default=True)
    applet = cls(*args, **kwargs)
    applet.run()
