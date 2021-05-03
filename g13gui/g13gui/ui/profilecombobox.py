import gi

from g13gui.observer.gtkobserver import GtkObserver
from g13gui.observer.subject import ChangeType

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, GObject, Gdk


def AlphabeticalSort(model, a, b, userData):
    print('AlphabeticalSort %s <=> %s' % (a, b))
    if a == b:
        return 0
    if a < b:
        return -1
    return 1


class ProfileComboBox(Gtk.ComboBoxText, GtkObserver):
    def __init__(self, prefs):
        Gtk.ComboBoxText.__init__(self)
        GtkObserver.__init__(self)

        self._prefs = prefs
        self._prefs.registerObserver(self, {'profile', 'selectedProfile'})
        self._isUpdating = False
        self._ignoreSelectionChange = False

        self._model = self.get_model()
        self._model.set_sort_column_id(0, Gtk.SortType.ASCENDING)
        self._model.set_default_sort_func(AlphabeticalSort)
        self.connect("changed", self._profileChanged)

        self.update()

    def _profileChanged(self, widget):
        selectedProfile = self.get_active_text()
        if selectedProfile:
            self._ignoreSelectionChange = True
            self._prefs.setSelectedProfile(selectedProfile)
            self._ignoreSelectionChange = False

    def update(self):
        profiles = self._prefs.profileNames()
        selected = self._prefs.selectedProfileName()

        self._model.clear()
        row = 0

        for name in profiles:
            self._model.append([name, name])
            if name == selected:
                self.set_active(row)
            row = row + 1

    def gtkSubjectChanged(self, subject, changeType, key, data=None):
        if key == 'profile':
            name = list(data.keys())[0]
            if changeType == ChangeType.ADD:
                self._model.append([name, name])

        if key == 'selectedProfile' and not self._ignoreSelectionChange:
            self.update()
