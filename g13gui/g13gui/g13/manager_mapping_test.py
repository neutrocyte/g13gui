from g13gui.model.prefs import Preferences
from g13gui.g13.manager import Manager


if __name__ == '__main__':
    prefs = Preferences()
    manager = Manager(prefs)
    manager.run()
