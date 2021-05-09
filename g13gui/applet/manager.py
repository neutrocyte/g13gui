import gi
import dbus
import dbus.service
import dbus.mainloop.glib
import time

from builtins import property

from g13gui.observer.subject import Subject
from g13gui.observer.subject import ChangeType
from g13gui.applet.switcher import Switcher
from g13gui.g13.common import G13Keys

gi.require_version('GLib', '2.0')
from gi.repository import GLib


class AppletManager(dbus.service.Object, Subject):
    INTERFACE_NAME = 'com.theonelab.g13.AppletManager'
    BUS_NAME = 'com.theonelab.g13.AppletManager'
    BUS_PATH = '/com/theonelab/g13/AppletManager'

    def __init__(self, manager, prefs):
        self._bus = dbus.SessionBus()
        self._busName = dbus.service.BusName(AppletManager.BUS_NAME, self._bus)
        dbus.service.Object.__init__(self, self._bus,
                                     AppletManager.BUS_PATH)
        Subject.__init__(self)

        self._manager = manager
        self._prefs = prefs

        # [name] -> (sender, proxy)
        self._applets = {}

        self._switcher = Switcher(self)
        self._activeApplet = self._switcher

        self._applets['Switcher'] = (self._switcher, self._switcher)
        self.addChange(ChangeType.ADD, 'applet', 'Switcher')
        self.notifyChanged()

    @property
    def activeApplet(self):
        return self._activeApplet

    @activeApplet.setter
    def activeApplet(self, appletName):
        (name, appletProxy) = self._applets[appletName]
        self._activeApplet.Unpresent()
        self.setProperty('activeApplet', appletProxy)
        self.onPresent()

    def raiseSwitcher(self):
        self._activeApplet = self._switcher
        self.onPresent()

    @property
    def appletNames(self):
        return self._applets.keys()

    def _updateLCD(self, frame):
        self._manager.setLCDBuffer(frame)

    def onPresent(self):
        frame = self._activeApplet.Present(time.time(), byte_arrays=True)
        frame = bytes(frame)
        self._updateLCD(frame)

    def onKeyPressed(self, key):
        # Swap to the switcher
        if key == G13Keys.BD:
            self.activeApplet = 'Switcher'
            return

        frame = self._activeApplet.KeyPressed(time.time(), key.value['bit'])
        self._updateLCD(frame)

    def onKeyReleased(self, key):
        frame = self._activeApplet.KeyReleased(time.time(), key.value['bit'])
        self._updateLCD(frame)

    def _registerApplet(self, name, sender):
        proxy = self._bus.get_object(sender, '/com/theonelab/g13/Applet')
        self._applets[name] = (sender, proxy)
        self.addChange(ChangeType.ADD, 'applet', name)
        self.notifyChanged()

    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='s', sender_keyword='sender')
    def Register(self, name, sender):
        if sender is None:
            print('Attempt to register None as sender applet!')
            return False

        print('Registered applet %s as %s' % (name, sender))
        GLib.idle_add(self._registerApplet, str(name), sender)

    def _presentScreen(self, screen, sender):
        self._updateLCD(screen)

    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='ay', sender_keyword='sender',
                         byte_arrays=True)
    def Present(self, screen, sender):
        if self._activeApplet.bus_name != sender:
            print('Sender %s is not the active applet.' % (sender))
            return
        GLib.idle_add(self._presentScreen, screen, sender)

    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         out_signature='b',
                         sender_keyword='sender')
    def Ping(self, sender):
        if sender not in [s[0] for s in self._applets.values()]:
            print('Sender %s is not in the registered list of applets.' % (sender))
            return False
        return True

    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         out_signature='as',
                         sender_keyword='sender')
    def GetProfiles(self, sender):
        if sender not in [s[0] for s in self._applets.values()]:
            print('Sender %s is not in the registered list of applets.' % (sender))
            return []
        return self._prefs.profileNames()

    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         out_signature='s',
                         sender_keyword='sender')
    def GetSelectedProfile(self, sender):
        if sender not in [s[0] for s in self._applets.values()]:
            print('Sender %s is not in the registered list of applets.' % (sender))
            return ''
        return self._prefs.selectedProfileName()

    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='s', out_signature='b',
                         sender_keyword='sender')
    def SetSelectedProfile(self, profileName, sender):
        if self._activeApplet.bus_name != sender:
            print('Sender %s is not the active applet' % (sender))
            return False
        if profileName not in self._prefs.profileNames():
            print('Sender %s attempted to set nonexistant profile %s' %
                  (sender, profileName))
            return False

        GLib.idle_add(self._prefs.setSelectedProfile, profileName)
