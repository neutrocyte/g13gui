from builtins import property

from g13gui.observer.subject import Subject
from g13gui.observer.subject import ChangeType
import g13gui.model.bindings as bindings


class BindingProfile(Subject):
    def __init__(self, dict=None):
        Subject.__init__(self)
        self.initDefaults()
        if dict:
            self.loadFromDict(dict)

    def initDefaults(self):
        self._stickMode = bindings.StickMode.KEYS
        self._stickRegions = bindings.DEFAULT_STICK_REGIONS.copy()
        self._stickRegionBindings = bindings.DEFAULT_STICK_REGION_BINDINGS.copy()
        self._keyBindings = bindings.DEFAULT_KEY_BINDINGS.copy()
        self._lcdColor = bindings.DEFAULT_LCD_COLOR

    @property
    def lcdColor(self):
        return self._lcdColor

    @property
    def stickMode(self):
        return self._stickMode

    def stickRegions(self):
        return self._stickRegions

    def keyBinding(self, gkey):
        if gkey in self._stickRegions.keys():
            if gkey in self._stickRegionBindings.keys():
                return self._stickRegionBindings[gkey]

        if gkey in self._keyBindings.keys():
            return self._keyBindings[gkey]

        return []

    def _setLCDColor(self, red, green, blue):
        self.setProperty('lcdColor', (red, green, blue), notify=False)

    @lcdColor.setter
    def lcdColor(self, red, green, blue):
        self._setLCDColor(red, green, blue)
        self.notifyChanged()

    def _setStickMode(self, stickmode):
        if stickmode not in bindings.ALL_STICK_MODES:
            raise ValueError('stickmode must be one of %s' %
                             (bindings.ALL_STICK_MODES))

        self._stickMode = stickmode
        self.addChange(ChangeType.MODIFY, 'stickmode', stickmode)

    @stickMode.setter
    def stickMode(self, stickmode):
        self._setStickMode(stickmode)
        self.notifyChanged()

    def _bindKey(self, gkey, keybinding):
        if gkey in self._stickRegions.keys():
            self._stickRegionBindings[gkey] = keybinding
        else:
            self._keyBindings[gkey] = keybinding
        self.addChange(ChangeType.MODIFY, gkey, keybinding)

    def bindKey(self, gkey, keybinding):
        self._bindKey(gkey, keybinding)
        self.notifyChanged()

    def loadFromDict(self, dict):
        self._lcdColor = dict['lcdcolor']
        self._stickMode = dict['stickMode']
        self._stickRegions = dict['stickRegions'].copy()
        self._stickRegionBindings = dict['stickRegionBindings'].copy()
        self._keyBindings = dict['keyBindings'].copy()

    def saveToDict(self):
        return {
            'lcdcolor': self._lcdColor,
            'stickMode': self._stickMode,
            'stickRegions': self._stickRegions.copy(),
            'stickRegionBindings': self._stickRegionBindings.copy(),
            'keyBindings': self._keyBindings.copy()
        }
