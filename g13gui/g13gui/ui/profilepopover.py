import gi
import enum

import g13gui.model.bindings as bindings
from g13gui.observer.gtkobserver import GtkObserver
from g13gui.model.bindingprofile import BindingProfile
from g13gui.model.bindings import StickMode
from g13gui.model.bindings import ALL_STICK_MODES

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, GObject, Gdk


class ProfilePopoverMode(enum.Enum):
    EDIT = 'edit'
    ADD = 'add'


class ProfilePopover(Gtk.Popover, GtkObserver):
    def __init__(self, prefs, mode=ProfilePopoverMode.EDIT):
        Gtk.Popover.__init__(self)
        GtkObserver.__init__(self)

        self._prefs = prefs
        self._mode = mode
        self._lastRow = 0

        self.build()
        self.connect('show', self.shown)

    def updateFromPrefs(self):
        self._profileName.set_text(self._prefs.selectedProfileName())

        profile = self._prefs.selectedProfile()
        lcdColor = profile.lcdColor
        self._lcdColorButton.set_rgba(Gdk.RGBA(*lcdColor, alpha=1.0))

        stickMode = profile.stickMode
        activeIndex = sorted(list(ALL_STICK_MODES)).index(stickMode)
        self._stickModeCombo.set_active(activeIndex)

    def commitToPrefs(self):
        pass

    def addRow(self, widget, labelText=None):
        if labelText:
            label = Gtk.Label()
            label.set_text(labelText)
            self._grid.attach(label, 1, self._lastRow, 1, 1)
            self._grid.attach(widget, 2, self._lastRow, 1, 1)
        else:
            self._grid.attach(widget, 1, self._lastRow, 2, 1)
        self._lastRow += 1

    def build(self):
        self._grid = Gtk.Grid()
        self._grid.set_row_spacing(6)
        self._grid.set_column_spacing(10)
        self._grid.set_border_width(6)
        self.add(self._grid)

        self._profileName = Gtk.Entry()
        self._profileName.set_can_focus(True)
        self._profileName.set_activates_default(True)
        self.addRow(self._profileName, 'Profile Name')

        self._lcdColorButton = Gtk.ColorButton()
        self._lcdColorButton.set_use_alpha(False)
        self._lcdColorButton.set_rgba(Gdk.RGBA(*bindings.DEFAULT_LCD_COLOR))
        self._lcdColorButton.set_title('LCD Color')
        self.addRow(self._lcdColorButton, 'LCD Color')

        self._stickModeCombo = Gtk.ComboBoxText()
        for mode in sorted(list(ALL_STICK_MODES)):
            self._stickModeCombo.append_text(mode.capitalize())
        self._stickModeCombo.set_active(1)
        self.addRow(self._stickModeCombo, 'Joystick Mode')

        commitButton = Gtk.Button()
        commitButton.set_receives_default(True)
        commitButton.set_can_default(True)
        commitButton.connect('clicked', self.commitClicked)

        if self._mode == ProfilePopoverMode.EDIT:
            commitButton.set_label('Update')
            commitButton.get_style_context().add_class('suggested-action')
            self.addRow(commitButton)

            removeButton = Gtk.Button()
            removeButton.set_label('Remove')
            removeButton.connect('clicked', self.removeClicked)
            removeButton.get_style_context().add_class('destructive-action')
            self.addRow(removeButton)
        else:
            commitButton.set_label('Add')
            commitButton.get_style_context().add_class('suggested-action')
            self.addRow(commitButton)

        self._grid.show_all()

    def commitClicked(self, widget):
        lcdColor = self._lcdColorButton.get_rgba()
        lcdColor = (lcdColor.red, lcdColor.green, lcdColor.blue)
        profileName = self._profileName.get_text()
        stickMode = self._stickModeCombo.get_active_text()

        profile = None
        if self._mode == ProfilePopoverMode.ADD:
            profile = BindingProfile()
            self._prefs.addProfile(profileName, profile)
        else:
            profile = self._prefs.selectedProfile()

        profile.lcdColor = lcdColor
        profile.stickMode = stickMode.upper()

        self.hide()

    def removeClicked(self, widget):
        pass

    def shown(self, widget):
        self._profileName.grab_focus()
        if self._mode == ProfilePopoverMode.EDIT:
            self.updateFromPrefs()
