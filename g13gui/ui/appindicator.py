import gi

from g13gui.common import PROGNAME
from g13gui.observer.gtkobserver import GtkObserver
from g13gui.observer.subject import ChangeType
from g13gui.ui.mainwindow import MainWindow

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, GObject
from gi.repository import AppIndicator3 as indicator


class AppIndicator(GtkObserver):
    def __init__(self, app, prefs):
        GtkObserver.__init__(self)

        self._app = app
        self._prefs = prefs

        self._initIndicator()

        self._menu = Gtk.Menu()
        self._menuItems = []
        self._indicator.set_menu(self._menu)

        self._rebuilding = False

        self._prefs.registerObserver(self, {'selectedProfile'})
        self.changeTrigger(self.onSelectedProfileChanged,
                           keys={'selectedProfile'})

        self._rebuildMenu()

    def _initIndicator(self):
        self._indicator = indicator.Indicator.new(
            PROGNAME, "g13gui", indicator.IndicatorCategory.OTHER)
        self._indicator.set_status(indicator.IndicatorStatus.ACTIVE)

    def _removeAllMenuItems(self):
        for item in self._menuItems:
            self._menu.remove(item)
        self._menuItems = []

    def _attachMenuItem(self, item):
        self._menu.append(item)
        self._menuItems.append(item)

    def _rebuildMenu(self):
        if self._rebuilding:
            return

        self._rebuilding = True
        self._removeAllMenuItems()
        profileNames = sorted(self._prefs.profileNames())
        selectedProfile = self._prefs.selectedProfileName()

        for name in profileNames:
            item = Gtk.CheckMenuItem(name)
            item.set_draw_as_radio(True)
            item.connect('activate', self.changeProfile)
            if name == selectedProfile:
                item.set_active(True)
            self._attachMenuItem(item)

        sep = Gtk.SeparatorMenuItem()
        self._attachMenuItem(sep)

        mainWindowItem = Gtk.MenuItem('Show g13 Configurator')
        mainWindowItem.connect('activate', self.showMainWindow)
        self._attachMenuItem(mainWindowItem)

        sep = Gtk.SeparatorMenuItem()
        self._attachMenuItem(sep)

        quitItem = Gtk.MenuItem('Quit')
        quitItem.connect('activate', self.onQuit)
        self._attachMenuItem(quitItem)

        self._menu.show_all()
        self._rebuilding = False

    def showMainWindow(self, menuItem):
        self._app.showMainWindow()

    def onQuit(self, menuItem):
        self._app.do_shutdown()

    def changeProfile(self, menuItem):
        self._prefs.setSelectedProfile(menuItem.get_label())

    def onSelectedProfileChanged(self, subject, changeType, key, data):
        self._rebuildMenu()
