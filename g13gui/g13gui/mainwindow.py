#!/usr/bin/python

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

from bindings import G13D_TO_GDK_KEYBINDS
from bindings import G13_KEYS
from bindingprofile import BindingProfile
from buttonmenu import ButtonMenu

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)

        default_profile = BindingProfile()
        default_profile.registerObserver(self)
        self._profiles = {'Default Profile': default_profile}
        self._currentProfile = self._profiles['Default Profile']

        self.headerBar = Gtk.HeaderBar()
        self.headerBar.set_title("G13 Configurator")
        self.headerBar.set_show_close_button(True)

        self.profileComboBox = Gtk.ComboBoxText()
        self.headerBar.add(self.profileComboBox)
        addProfileButton = Gtk.Button.new_from_icon_name("add", 1)
        self.headerBar.add(addProfileButton)

        Gtk.Window.set_default_size(self, 640, 480)
        Gtk.Window.set_titlebar(self, self.headerBar)

        self.box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.add(self.box)

        self.setupG13ButtonGrid()
        self.updateProfileBox()

    def updateProfileBox(self):
        self.profileComboBox.remove_all()
        row = 0
        for profileName in self._profiles.keys():
            self.profileComboBox.append_text(profileName)

            if self._profiles[profileName] == self._currentProfile:
                print("Set active profile to %d (%s)" % (row, profileName))
                self.profileComboBox.set_active(row)

            row = row + 1

    def setupG13ButtonGrid(self):
        self.lcdButtons = Gtk.Box(spacing=3, orientation=Gtk.Orientation.HORIZONTAL)
        self.box.pack_start(self.lcdButtons, True, True, 6)

        self.mButtons = Gtk.Box(spacing=3, orientation=Gtk.Orientation.HORIZONTAL)
        self.box.pack_start(self.mButtons, True, True, 6)

        self.keyGrid = Gtk.Grid()
        self.keyGrid.set_row_spacing(3)
        self.keyGrid.set_column_spacing(3)
        self.box.pack_start(self.keyGrid, True, True, 6)

        self.stickGrid = Gtk.Grid()
        self.stickGrid.set_row_spacing(3)
        self.stickGrid.set_column_spacing(3)
        self.box.pack_start(self.stickGrid, False, False, 6)

        self.g13Buttons = {}

        self.lcdButtons.pack_start(self.newG13Button('BD'), True, True, 6)
        self.lcdButtons.pack_start(self.newG13Button('L1'), True, True, 6)
        self.lcdButtons.pack_start(self.newG13Button('L2'), True, True, 6)
        self.lcdButtons.pack_start(self.newG13Button('L3'), True, True, 6)
        self.lcdButtons.pack_start(self.newG13Button('L4'), True, True, 6)
        self.lcdButtons.pack_start(self.newG13Button('LIGHT'), True, True, 6)

        self.mButtons.pack_start(self.newG13Button('M1'), True, True, 6)
        self.mButtons.pack_start(self.newG13Button('M2'), True, True, 6)
        self.mButtons.pack_start(self.newG13Button('M3'), True, True, 6)
        self.mButtons.pack_start(self.newG13Button('MR'), True, True, 6)

        # G1 to G14
        self._buttonNum = 1
        for row in range(0, 2):
            for col in range(0, 7):
                self.keyGrid.attach(self.newG13NumberedButton(),
                                    col, row, 1, 1)

        # G15 to G19
        self.keyGrid.attach(self.newG13NumberedButton(), 1, 3, 1, 1)
        self.keyGrid.attach(self.newG13NumberedButton(), 2, 3, 1, 1)
        self.keyGrid.attach(self.newG13NumberedButton(), 3, 3, 1, 1)
        self.keyGrid.attach(self.newG13NumberedButton(), 4, 3, 1, 1)
        self.keyGrid.attach(self.newG13NumberedButton(), 5, 3, 1, 1)

        # G20 to G22
        self.keyGrid.attach(self.newG13NumberedButton(), 2, 4, 1, 1)
        self.keyGrid.attach(self.newG13NumberedButton(), 3, 4, 1, 1)
        self.keyGrid.attach(self.newG13NumberedButton(), 4, 4, 1, 1)

        self.stickGrid.attach(self.newG13Button("STICK_UP"),    4, 0, 1, 1)
        self.stickGrid.attach(self.newG13Button("LEFT"),        2, 1, 1, 1)
        self.stickGrid.attach(self.newG13Button("STICK_LEFT"),  3, 1, 1, 1)
        self.stickGrid.attach(self.newG13Button("TOP"),         4, 1, 1, 1)
        self.stickGrid.attach(self.newG13Button("STICK_RIGHT"), 5, 1, 1, 1)
        self.stickGrid.attach(self.newG13Button("STICK_DOWN"),  4, 2, 1, 1)
        self.stickGrid.attach(self.newG13Button("DOWN"),        4, 3, 1, 1)

    def newG13NumberedButton(self):
        button = self.newG13Button('G' + str(self._buttonNum))
        self._buttonNum = self._buttonNum + 1
        return button

    def newG13Button(self, name):
        popover = ButtonMenu(self._currentProfile, name)
        button = Gtk.MenuButton(popover=popover)
        self.g13Buttons[name] = button
        self.updateG13Button(name)

        return button

    def updateG13Button(self, name):
        button = self.g13Buttons[name]
        children = button.get_children()

        if len(children) > 0:
            button.remove(children[0])

        bindings = self._currentProfile.getBoundKey(name)

        if len(bindings) > 0:
            keybinds = [G13D_TO_GDK_KEYBINDS[binding] for binding in bindings]
            accelerator = '+'.join(keybinds)
            shortcut = Gtk.ShortcutsShortcut(
                shortcut_type=Gtk.ShortcutType.ACCELERATOR,
                accelerator=accelerator)
            shortcut.set_halign(Gtk.Align.CENTER)
            button.add(shortcut)
        else:
            label = Gtk.Label(name)
            button.add(label)

        button.show_all()

    def on_changed(self, profile):
        for key in G13_KEYS:
            self.updateG13Button(key)

        print("Profile updated to:")
        print(self._currentProfile.generateConfigString())
