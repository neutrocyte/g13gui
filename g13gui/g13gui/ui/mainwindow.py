#!/usr/bin/python

import gi

import g13gui.ui as ui

from g13gui.observer.gtkobserver import GtkObserver

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GObject


class MainWindow(Gtk.Window, GtkObserver):
    def __init__(self, workerQueue, prefs):
        Gtk.Window.__init__(self)
        GtkObserver.__init__(self)

        self.set_default_size(640, 480)
        geometry = Gdk.Geometry()
        geometry.max_width = 640
        geometry.max_height = 480
        self.set_geometry_hints(None, geometry, Gdk.WindowHints.MAX_SIZE)

        self._workerQueue = workerQueue
        self._prefs = prefs
        self._prefs.registerObserver(self, 'selectedProfile')
        self._prefs.selectedProfile().registerObserver(self)
        self._lastProfileName = self._prefs.selectedProfileName()

        self.setupHeaderBar()

        self._box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self._box.set_border_width(6)
        self.add(self._box)

        self._infoBar = Gtk.InfoBar()
        self._infoBar.set_no_show_all(True)
        self._infoBarLabel = Gtk.Label()
        self._infoBar.get_content_area().add(self._infoBarLabel)
        self._infoBarLabel.show()
        self._box.add(self._infoBar)

        self.setupG13ButtonGrid()

    def gtkSubjectChanged(self, subject, changeType, key, data=None):
        print('Subject changed! Need to save!')
        pass

    def setupHeaderBar(self):
        self._headerBar = Gtk.HeaderBar()
        self._headerBar.set_title("G13 Configurator")
        self._headerBar.set_show_close_button(True)

        self._profileComboBox = ui.ProfileComboBox(self._prefs)
        self._profileComboBox.connect('changed', self._profileChanged)
        self._headerBar.add(self._profileComboBox)

        addProfileButton = Gtk.MenuButton.new()
        addProfileButton.add(Gtk.Image.new_from_icon_name(
            "document-new-symbolic", 1))
        addProfilePopover = ui.ProfilePopover(self._prefs,
                                              mode=ui.ProfilePopoverMode.ADD)
        addProfileButton.set_popover(addProfilePopover)
        self._headerBar.add(addProfileButton)

        editProfileButton = Gtk.MenuButton.new()
        editProfileButton.add(
            Gtk.Image.new_from_icon_name('document-edit-symbolic', 1))
        editProfilePopover = ui.ProfilePopover(self._prefs,
                                               mode=ui.ProfilePopoverMode.EDIT)
        editProfileButton.set_popover(editProfilePopover)
        self._headerBar.add(editProfileButton)

        self._uploadButton = Gtk.Button.new_from_icon_name(
            "document-send-symbolic", 1)
        self._uploadButton.connect("clicked", self.uploadClicked)
        self._headerBar.add(self._uploadButton)

        Gtk.Window.set_titlebar(self, self._headerBar)

    @GObject.Signal(name='daemon-connection-changed', arg_types=(bool,))
    def daemonConnectionChanged(self, connected):
        self._connected = connected
        if connected:
            self._uploadButton.set_state_flags(Gtk.StateFlags.NORMAL, True)
            self._infoBar.hide()
            self._doUpload()
        else:
            self._uploadButton.set_state_flags(Gtk.StateFlags.INSENSITIVE,
                                               True)
            self._infoBar.set_message_type(Gtk.MessageType.WARNING)
            self._infoBarLabel.set_text(
                'The G13 user space driver is not running. '
                'Attempting to reconnect.')
            self._infoBar.show()

    @GObject.Signal(name='uploading', arg_types=(float,))
    def uploadStatusChanged(self, percentage):
        if percentage < 1.0:
            self._infoBar.set_message_type(Gtk.MessageType.INFO)
            self._infoBarLabel.set_text('Uploading to the G13...')
            self._infoBar.show()
        else:
            self._infoBar.hide()

    def _profileChanged(self, widget):
        self._doUpload()

    def uploadClicked(self, widget):
        self._doUpload()
        self._doSave()

    def setupG13ButtonGrid(self):
        self._mButtons = Gtk.ButtonBox(
            spacing=3,
            orientation=Gtk.Orientation.HORIZONTAL,
            baseline_position=Gtk.BaselinePosition.CENTER)
        self._mButtons.set_layout(Gtk.ButtonBoxStyle.CENTER)
        self._box.pack_start(self._mButtons, False, False, 6)

        self._keyGrid = Gtk.Grid()
        self._keyGrid.set_hexpand(False)
        self._keyGrid.set_vexpand(False)
        self._keyGrid.set_row_spacing(3)
        self._keyGrid.set_column_spacing(3)
        self._box.pack_start(self._keyGrid, False, False, 6)

        self._stickGrid = Gtk.Grid()
        self._stickGrid.set_row_spacing(3)
        self._stickGrid.set_column_spacing(3)
        self._box.pack_start(self._stickGrid, False, False, 6)

        self._g13Buttons = {}

        self._mButtons.pack_start(self.newG13Button('M1'), False, False, 6)
        self._mButtons.pack_start(self.newG13Button('M2'), False, False, 6)
        self._mButtons.pack_start(self.newG13Button('M3'), False, False, 6)

        # G1 to G14
        self._buttonNum = 1
        for row in range(0, 2):
            for col in range(0, 7):
                self._keyGrid.attach(self.newG13NumberedButton(),
                                     col, row, 1, 1)

        # G15 to G19
        self._keyGrid.attach(self.newG13NumberedButton(), 1, 3, 1, 1)
        self._keyGrid.attach(self.newG13NumberedButton(), 2, 3, 1, 1)
        self._keyGrid.attach(self.newG13NumberedButton(), 3, 3, 1, 1)
        self._keyGrid.attach(self.newG13NumberedButton(), 4, 3, 1, 1)
        self._keyGrid.attach(self.newG13NumberedButton(), 5, 3, 1, 1)

        # G20 to G22
        self._keyGrid.attach(self.newG13NumberedButton(), 2, 4, 1, 1)
        self._keyGrid.attach(self.newG13NumberedButton(), 3, 4, 1, 1)
        self._keyGrid.attach(self.newG13NumberedButton(), 4, 4, 1, 1)

        self._stickGrid.attach(self.newG13Button("STICK_UP"),    4, 0, 1, 1)
        self._stickGrid.attach(self.newG13Button("THUMB_LEFT"),  2, 1, 1, 1)
        self._stickGrid.attach(self.newG13Button("STICK_LEFT"),  3, 1, 1, 1)
        self._stickGrid.attach(self.newG13Button("THUMB_STICK"), 4, 1, 1, 1)
        self._stickGrid.attach(self.newG13Button("STICK_RIGHT"), 5, 1, 1, 1)
        self._stickGrid.attach(self.newG13Button("STICK_DOWN"),  4, 2, 1, 1)
        self._stickGrid.attach(self.newG13Button("THUMB_DOWN"),  4, 3, 1, 1)

    def newG13NumberedButton(self):
        button = self.newG13Button('G' + str(self._buttonNum))
        self._buttonNum = self._buttonNum + 1
        return button

    def newG13Button(self, name):
        button = ui.G13Button(self._prefs, name)
        self._g13Buttons[name] = button
        return button
