#!/usr/bin/python3

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk
from gi.repository import Gdk

from bindings import GDK_TO_G13D_KEYBINDS
from bindings import G13D_TO_GDK_KEYBINDS
from bindings import G13DKeyIsModifier


MAX_DELAY_BETWEEN_PRESSES_MILLIS = 250


class ButtonMenu(Gtk.Popover):
    def __init__(self, profile, buttonName):
        Gtk.Popover.__init__(self)

        self._profile = profile
        self._buttonName = buttonName
        self._currentBindings = self._profile.getBoundKey(buttonName)
        self._bindingBox = None
        self._modifiers = {}
        self._consonantKey = None
        self._lastPressTime = 0

        self._box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.add(self._box)

        label = Gtk.Label()
        label.set_markup("<b>" + buttonName + "</b>")
        self._box.pack_start(label, True, True, 6)

        button = Gtk.Button(label="Clear Binding")
        self._box.pack_start(button, True, True, 6)

        self._box.show_all()

        self.connect("key-press-event", self.keypress)
        self.connect("key-release-event", self.keyrelease)
        self.connect("show", self.shown)
        self.connect("closed", self.closed)
        button.connect("pressed", self.clear)

        self.rebuildBindingDisplay()

    def shown(self, widget):
        Gdk.keyboard_grab(self.get_window(), False, Gdk.CURRENT_TIME)

    def rebuildBindingDisplay(self):
        if self._bindingBox:
            self._box.remove(self._bindingBox)

        self._bindingBox = Gtk.Box(spacing=0, orientation=Gtk.Orientation.VERTICAL)
        self._box.pack_start(self._bindingBox, True, True, 6)
        self._box.reorder_child(self._bindingBox, 1)

        if len(self._currentBindings) > 0:
            keybinds = [G13D_TO_GDK_KEYBINDS[binding] for binding in self._currentBindings]
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
        print("Keypressed! %s, %s" % (eventKey.keyval, Gdk.keyval_name(eventKey.keyval)))

        if eventKey.time - self._lastPressTime > MAX_DELAY_BETWEEN_PRESSES_MILLIS:
            self._modifiers = {}
            self._consonantKey = None

        binding = Gdk.keyval_name(eventKey.keyval)
        if len(binding) == 1:
            binding = binding.upper()

        if binding == 'Meta_L':
            binding = 'Alt_L'
        if binding == 'Meta_R':
            binding = 'Alt_R'
        binding = GDK_TO_G13D_KEYBINDS[binding]
        print('Binding is %s' % (binding))

        if G13DKeyIsModifier(binding):
            self._modifiers[binding] = True
            print("Modifiers are now %s" % (repr(self._modifiers.keys())))
        else:
            self._consonantKey = binding

        self._lastPressTime = eventKey.time

    def keyrelease(self, buttonMenu, eventKey):
        self._currentBindings = [modifier for modifier in self._modifiers.keys()]
        if self._consonantKey:
            self._currentBindings = self._currentBindings + [self._consonantKey]

        self.rebuildBindingDisplay()
        print("Bindings are now %s" % (self._currentBindings))

    def clear(self, button):
        self._currentBindings = []
        self.rebuildBindingDisplay()

    def closed(self, buttonMenu):
        self._profile.bindKey(self._buttonName, self._currentBindings)
        self.hide()
