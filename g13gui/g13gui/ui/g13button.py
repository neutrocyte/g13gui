import gi

import g13gui.ui as ui
from g13gui.observer import GtkObserver
from g13gui.model.bindings import G13ToGDK

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, GObject, Gdk


class G13Button(Gtk.MenuButton, GtkObserver):
    def __init__(self, prefs, g13KeyName):
        Gtk.MenuButton.__init__(self)
        GtkObserver.__init__(self)

        self._prefs = prefs
        self._prefs.registerObserver(self, {'selectedProfile'})
        self._keyName = g13KeyName
        self._lastProfileName = None

        self._popover = ui.G13ButtonPopover(self, self._prefs, self._keyName)
        self.set_popover(self._popover)

        _image = Gtk.Image.new_from_file(g13KeyName + '.png')
        self.get_style_context().add_class('flat')

        self.set_can_default(False)
        self.updateProfileRegistration()
        self.updateBindingDisplay()

    def updateProfileRegistration(self):
        if self._lastProfileName:
            if self._lastProfileName in self._prefs.profileNames():
                lastProfile = self._prefs.profiles(self._lastProfileName)
                lastProfile.removeObserver(self)

        self._prefs.selectedProfile().registerObserver(self, {self._keyName})

    def _removeChild(self):
        child = self.get_child()
        if child:
            self.remove(child)

    def updateBindingDisplay(self):
        self._removeChild()
        bindings = self._prefs.selectedProfile().keyBinding(self._keyName)

        if len(bindings) > 0:
            keybinds = G13ToGDK(bindings)
            accelerator = '+'.join(keybinds)
            shortcut = Gtk.ShortcutsShortcut(
                shortcut_type=Gtk.ShortcutType.ACCELERATOR,
                accelerator=accelerator)
            shortcut.set_halign(Gtk.Align.CENTER)
            self.add(shortcut)
        else:
            label = Gtk.Label(self._keyName)
            self.add(label)

        self.show_all()

    def gtkSubjectChanged(self, subject, changeType, key, data=None):
        if key == 'selectedProfile':
            self.updateProfileRegistration()
            self.updateBindingDisplay()
        elif key == self._keyName:
            self.updateBindingDisplay()
