import gi

from g13gui.observer import GtkObserver

from g13gui.model.bindings import G13ToGDK
from g13gui.model.bindings import GDKToG13
from g13gui.model.bindings import G13DKeyIsModifier

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, GObject, Gdk


MAX_DELAY_BETWEEN_PRESSES_MILLIS = 250


class G13ButtonPopover(Gtk.Popover, GtkObserver):
    def __init__(self, buttonOwner, prefs, keyName):
        Gtk.Popover.__init__(self)
        GtkObserver.__init__(self)

        self._prefs = prefs
        self._prefs.registerObserver(self, {'selectedProfile'})
        self._keyName = keyName

        self._modifiers = set()
        self._consonantKey = None
        self._lastPressTime = 0

        self.set_relative_to(buttonOwner)
        self.updateBinding()
        self.build()

    def updateBinding(self):
        selectedProfile = self._prefs.selectedProfile()
        self._currentBindings = selectedProfile.keyBinding(self._keyName)

    def gtkSubjectChanged(self, subject, changeType, key, data=None):
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

        self.connect("key-press-event", self.keypress)
        self.connect("key-release-event", self.keyrelease)
        self.connect("show", self.shown)
        self.connect("closed", self.closed)
        button.connect("pressed", self.clear)

        self.buildBindingDisplay()

    def shown(self, widget):
        self.grab_add()

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
            keybinds = G13ToGDK(self._currentBindings)
            accelerator = '+'.join(keybinds)
            shortcut = Gtk.ShortcutsShortcut(
                shortcut_type=Gtk.ShortcutType.ACCELERATOR,
                accelerator=accelerator)
            shortcut.set_halign(Gtk.Align.CENTER)
            self._bindingBox.pack_start(shortcut, True, True, 6)
        else:
            label = Gtk.Label()
            label.set_markup("<i>No binding. Press a key to bind.</i>")
            self._bindingBox.add(label)

        self._bindingBox.show_all()

    def keypress(self, buttonMenu, eventKey):
        pressDelta = eventKey.time - self._lastPressTime
        if pressDelta > MAX_DELAY_BETWEEN_PRESSES_MILLIS:
            self._modifiers = set()
            self._consonantKey = None

        binding = Gdk.keyval_name(eventKey.keyval)
        if len(binding) == 1:
            binding = binding.upper()
        if binding == 'Meta_L':
            binding = 'Alt_L'
        if binding == 'Meta_R':
            binding = 'Alt_R'

        binding = GDKToG13(binding)

        if G13DKeyIsModifier(binding):
            self._modifiers.add(binding)
        else:
            self._consonantKey = binding

        self._lastPressTime = eventKey.time
        return True

    def keyrelease(self, buttonMenu, eventKey):
        self._currentBindings = sorted(list(self._modifiers))
        if self._consonantKey:
            self._currentBindings += [self._consonantKey]
        self.rebuildBindingDisplay()
        self.hide()
        return True

    def clear(self, button):
        self._currentBindings = []
        self.rebuildBindingDisplay()
        self.hide()

    def closed(self, buttonMenu):
        self.grab_remove()
        self._prefs.selectedProfile().bindKey(self._keyName,
                                              self._currentBindings)
        self.hide()
