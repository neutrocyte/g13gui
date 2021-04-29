import json

import g13gui.model as model
from g13gui.common import PROFILES_CONFIG_PATH


class PreferencesStore(object):
    def getPrefs():
        try:
            with open(PROFILES_CONFIG_PATH, 'r') as f:
                data = f.read()
                prefsDict = json.loads(data)
                return model.Preferences(prefsDict)
        except:
            return model.Preferences()

    def storePrefs(prefs):
        prefsDict = prefs.saveToDict()

        with open(PROFILES_CONFIG_PATH, 'w') as f:
            f.write(json.dumps(prefsDict, default=str))
            f.flush()
