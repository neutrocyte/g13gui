import threading

from g13gui.ui.profilecombobox import ProfileComboBox
from g13gui.ui.profilepopover import ProfilePopover
from g13gui.ui.profilepopover import ProfilePopoverMode
from g13gui.ui.g13button import G13Button
from g13gui.observer.gtkobserver import GtkObserver
from g13gui.model.prefsstore import PreferencesStore

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GObject


class MainWindow(Gtk.ApplicationWindow, GtkObserver):
    def __init__(self, app, prefs, **kwargs):
        Gtk.ApplicationWindow.__init__(
            self,
            default_width=640,
            default_height=480,
            window_position=Gtk.WindowPosition.NONE,
            name='g13configurator',
            icon_name='g13configurator',
            application=app,
            **kwargs)
        GtkObserver.__init__(self)

        self._app = app
        self._prefs = prefs
        self._prefs.registerObserver(self, {'selectedProfile'})
        self._prefs.selectedProfile().registerObserver(self)
        self._lastProfileName = self._prefs.selectedProfileName()

        self.changeTrigger(self.onChangeTrigger)

        self.setupHeaderBar()

        self._box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self._box.set_border_width(6)
        self._box.set_margin_left(6)
        self._box.set_margin_right(6)
        self.add(self._box)

        self.setupG13ButtonGrid()

        self.set_resizable(False)

        self.show_all()

    def _updateProfileRegistration(self):
        lastProfile = self._prefs.profiles(self._lastProfileName)
        lastProfile.removeObserver(self)
        self._lastProfileName = self._prefs.selectedProfileName()
        self._prefs.selectedProfile().registerObserver(self)

    def onChangeTrigger(self, subject, changeType, key, data=None):
        if key == 'selectedProfile':
            self._updateProfileRegistration()

        t = threading.Thread(
            target=PreferencesStore.storePrefs,
            args=(self._prefs,),
            daemon=True)
        t.start()
        print('Detected change -- saving via %s' % repr(t))

    def setupHeaderBar(self):
        self._headerBar = Gtk.HeaderBar()
        self._headerBar.set_title("G13 Configurator")
        self._headerBar.set_show_close_button(True)

        self._profileComboBox = ProfileComboBox(self._prefs)
        self._headerBar.add(self._profileComboBox)

        addProfileButton = Gtk.MenuButton.new()
        addProfileButton.add(Gtk.Image.new_from_icon_name(
            "document-new-symbolic", 1))
        addProfilePopover = ProfilePopover(self._prefs,
                                           mode=ProfilePopoverMode.ADD)
        addProfileButton.set_popover(addProfilePopover)
        self._headerBar.add(addProfileButton)

        editProfileButton = Gtk.MenuButton.new()
        editProfileButton.add(
            Gtk.Image.new_from_icon_name('document-edit-symbolic', 1))
        editProfilePopover = ProfilePopover(self._prefs,
                                            mode=ProfilePopoverMode.EDIT)
        editProfileButton.set_popover(editProfilePopover)
        self._headerBar.add(editProfileButton)

        Gtk.Window.set_titlebar(self, self._headerBar)

    def setupG13ButtonGrid(self):
        self._mButtons = Gtk.ButtonBox(
            spacing=6,
            orientation=Gtk.Orientation.HORIZONTAL,
            baseline_position=Gtk.BaselinePosition.CENTER)
        self._mButtons.set_layout(Gtk.ButtonBoxStyle.CENTER)
        self._mButtons.set_hexpand(False)
        self._mButtons.set_vexpand(False)
        self._box.pack_start(self._mButtons, True, False, 6)

        self._keyGrid = Gtk.Grid()
        self._keyGrid.set_hexpand(False)
        self._keyGrid.set_vexpand(False)
        self._keyGrid.set_row_spacing(6)
        self._keyGrid.set_column_spacing(6)
        self._keyGrid.set_row_homogeneous(True)
        self._keyGrid.set_column_homogeneous(True)
        self._box.pack_start(self._keyGrid, True, False, 6)

        self._stickGrid = Gtk.Grid()
        self._stickGrid.set_hexpand(False)
        self._stickGrid.set_vexpand(False)
        self._stickGrid.set_row_spacing(6)
        self._stickGrid.set_column_spacing(6)
        self._stickGrid.set_row_homogeneous(True)
        self._stickGrid.set_column_homogeneous(True)
        self._box.pack_start(self._stickGrid, True, False, 6)

        self._g13Buttons = {}

        mrButton = self.newG13Button('MR')
        mrButton.set_sensitive(False)
        self._mButtons.pack_start(mrButton, False, False, 6)
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
        button = G13Button(self._prefs, name)
        self._g13Buttons[name] = button
        return button
