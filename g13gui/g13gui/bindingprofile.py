#!/usr/bin/python

import bindings

from observer import Subject
from observer import ChangeType


class BindingProfile(Subject):
    def __init__(self, dict=None):
        self.initDefaults()
        if dict:
            self.loadFromDict(dict)

    def initDefaults(self):
        self._stickMode = bindings.StickMode.KEYS
        self._stickRegions = bindings.DEFAULT_STICK_REGIONS
        self._stickRegionBindings = bindings.DEFAULT_STICK_REGION_BINDINGS
        self._keyBindings = bindings.DEFAULT_KEY_BINDINGS

    def stickMode(self):
        return self._stickMode

    def stickRegions(self):
        return self._stickRegions

    def keyBinding(self, gkey):
        gkey = gkey.upper()

        if gkey in self._stickRegions.keys():
            if gkey in self._stickRegionBindings.keys():
                return self._stickRegionBindings[gkey]

        if gkey in self._keyBindings.keys():
            return self._keyBindings[gkey]

        return []

    def _bindKey(self, gkey, keybinding):
        if gkey in self._stickRegions.keys():
            self._stickRegionBindings[gkey] = keybinding
        else:
            self._keyBindings[gkey] = keybinding
        self.addChange(ChangeType.MODIFY, gkey, keybinding)

    def bindKey(self, gkey, keybinding):
        self._bindKey(gkey, keybinding)
        self.notifyChanged()

    def _setStickMode(self, stickmode):
        if stickmode not in bindings.ALL_STICK_MODES:
            raise ValueError('stickmode must be one of %s' %
                             (bindings.ALL_STICK_MODES))

        self._stickMode = stickmode
        self.addChange(ChangeType.MODIFY, 'stickmode', stickmode)

    def setStickMode(self, stickmode):
        self._setStickMode(stickmode)
        self.notifyChanged()

    def toCommandString(self):
        commands = []

        for gkey, kbdkey in self._keyBindings.items():
            if len(kbdkey) > 0:
                keys = '+'.join(['KEY_' + key for key in kbdkey])
                commands.append("bind %s %s" % (gkey, keys))
            else:
                commands.append("unbind %s" % (gkey))

        if self._stickMode == bindings.StickMode.KEYS:
            for region, bounds in self._stickRegions.items():
                commands.append("stickzone add %s" % (region))
                commands.append("stickzone bounds %s %0.1f %0.1f %0.1f %0.1f" %
                                (region, *bounds))
                keys = ' '.join(['KEY_' + key for key in self._stickRegionBindings[region]])
                commands.append("stickzone action %s %s" % (region, keys))

        return '\n'.join(commands)

    def loadFromDict(self, dict):
        self._stickMode = dict['stickMode']
        self._stickRegions = dict['stickRegions']
        self._stickRegionBindings = dict['stickRegionBindings']
        self._keyBindings = dict['keyBindings']

    def saveToDict(self):
        return {
            'stickMode': self._stickMode,
            'stickRegions': self._stickRegions,
            'stickRegionBindings': self._stickRegionBindings,
            'keyBindings': self._keyBindings
        }
