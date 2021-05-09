import json
import threading

from g13gui.model.prefs import Preferences
from g13gui.common import PROFILES_CONFIG_PATH


class PreferencesStore(object):
    SaveLock = threading.Lock()

    def getPrefs():
        try:
            with open(PROFILES_CONFIG_PATH, 'r') as f:
                data = f.read()
                prefsDict = json.loads(data)
                return Preferences(prefsDict)
        except Exception as e:
            print('Unable to load preferences from %s: %s'
                  % (PROFILES_CONFIG_PATH, e))
            return Preferences()

    def storePrefs(prefs):
        with PreferencesStore.SaveLock:
            prefsDict = prefs.saveToDict()

            with open(PROFILES_CONFIG_PATH, 'w') as f:
                f.write(json.dumps(prefsDict, default=str))
                f.flush()
