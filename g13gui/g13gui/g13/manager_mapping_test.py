from g13gui.model.prefs import Preferences
from g13gui.g13.manager import DeviceManager


if __name__ == '__main__':
    prefs = Preferences()
    manager = DeviceManager(prefs)
    manager.run()
