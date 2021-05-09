import gi

from g13gui.observer.gtkobserver import GtkObserver
from g13gui.model.bindings import BindsToKeynames
from g13gui.model.bindings import KeycodeIsModifier
from g13gui.input import InputReader

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, GObject, Gdk, GLib


MAX_DELAY_BETWEEN_PRESSES_SECONDS = 0.250


class G13ButtonPopover(Gtk.Popover, GtkObserver):
    def __init__(self, buttonOwner, prefs, keyName):
        Gtk.Popover.__init__(self)
        GtkObserver.__init__(self)

        self._prefs = prefs
        self._prefs.registerObserver(self, {'selectedProfile'})
        self.changeTrigger(self.onSelectedProfileChanged,
                           keys={'selectedProfile'})

        self._inputReader = InputReader()
        self._inputReader.connect('evdev-key-pressed', self.keypress)
        self._inputReader.connect('evdev-key-released', self.keyrelease)
        self.connect('key-press-event', self.ignoreKeypress)

        self._keyName = keyName

        self._modifiers = set()
        self._consonantKey = None
        self._lastPressTime = 0

        self.set_relative_to(buttonOwner)
        self.updateBinding()
        self.build()

    def ignoreKeypress(self, *args, **kwargs):
        return True

    def updateBinding(self):
        selectedProfile = self._prefs.selectedProfile()
        self._currentBindings = selectedProfile.keyBinding(self._keyName)

    def onSelectedProfileChanged(self, subject, changeType, key, data):
        self.updateBinding()

    def build(self):
        self._box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self._box.set_border_width(6)
        self.add(self._box)

        label = Gtk.Label()
        label.set_markup("<b>" + self._keyName + "</b>")
        self._box.pack_start(label, True, True, 6)

        button = Gtk.Button(label="Clear Binding")
        button.set_can_focus(False)
        self._box.pack_start(button, True, True, 6)
        self._box.show_all()

        self.connect("show", self.shown)
        self.connect("closed", self.closed)
        button.connect("pressed", self.clear)

        self.buildBindingDisplay()

    def shown(self, widget):
        self._inputReader.capture()

    def rebuildBindingDisplay(self):
        if self._bindingBox:
            self._box.remove(self._bindingBox)

        self.buildBindingDisplay()

    def buildBindingDisplay(self):
        self._bindingBox = Gtk.Box(spacing=0,
                                   orientation=Gtk.Orientation.VERTICAL)
        self._box.pack_start(self._bindingBox, True, True, 6)
        self._box.reorder_child(self._bindingBox, 1)

        if len(self._currentBindings) > 0:
            keybinds = BindsToKeynames(self._currentBindings)
            accelerator = '+'.join(keybinds)
            label = Gtk.Label(accelerator)
            label.set_halign(Gtk.Align.CENTER)
            self._bindingBox.pack_start(label, True, True, 6)
        else:
            label = Gtk.Label()
            label.set_markup("<i>No binding. Press a key to bind.</i>")
            self._bindingBox.add(label)

        self._bindingBox.show_all()

    def keypress(self, obj, keyCode, timestamp):
        pressDelta = timestamp - self._lastPressTime
        if pressDelta > MAX_DELAY_BETWEEN_PRESSES_SECONDS:
            self._modifiers = set()
            self._consonantKey = None

        key = keyCode

        if KeycodeIsModifier(key):
            self._modifiers.add(key)
        else:
            self._consonantKey = key

        self._lastPressTime = timestamp

    def keyrelease(self, obj, keyCode, timestamp):
        self._currentBindings = sorted(list(self._modifiers))
        if self._consonantKey:
            self._currentBindings += [self._consonantKey]
        self.rebuildBindingDisplay()
        self.hide()

    def clear(self, button):
        self._currentBindings = []
        self.rebuildBindingDisplay()
        self.hide()

    def closed(self, buttonMenu):
        self._prefs.selectedProfile().bindKey(self._keyName,
                                              self._currentBindings)
        self.hide()
        self._inputReader.stop()
 
