#!/usr/bin/python

import bindings


class BindingProfile(object):
    def __init__(self):
        self._stickMode = bindings.GetStickModeNum('KEYS')
        self._stickRegions = bindings.DEFAULT_STICK_REGIONS
        self._stickRegionBindings = bindings.DEFAULT_STICK_REGION_BINDINGS
        self._keyBindings = bindings.DEFAULT_KEY_BINDINGS
        self._observers = []

    def registerObserver(self, observer):
        self._observers.append(observer)

    def getStickRegions(self):
        return self._stickRegions

    def getBoundKey(self, gkey):
        gkey = gkey.upper()

        if gkey in self._stickRegions.keys():
            if gkey in self._stickRegionBindings.keys():
                return self._stickRegionBindings[gkey]

        if gkey in self._keyBindings.keys():
            return self._keyBindings[gkey]

        return []

    def bindKey(self, gkey, keybinding):
        if gkey in self._stickRegions.keys():
            self._stickRegionBindings[gkey] = keybinding
            return

        self._keyBindings[gkey] = keybinding
        self._notify()

    def _notify(self):
        for observer in self._observers:
            observer.on_changed(self)

    def generateConfigString(self):
        commands = []

        for gkey, kbdkey in self._keyBindings.items():
            keys = ' '.join(['KEY_' + key for key in kbdkey])
            commands.append("bind %s %s" % (gkey, keys))

        if self._stickMode == bindings.GetStickModeNum('KEYS'):
            for region, bounds in self._stickRegions.items():
                commands.append("stickzone add %s" % (region))
                commands.append("stickzone bounds %s %0.1f %0.1f %0.1f %0.1f" % (region, bounds[0], bounds[1], bounds[2], bounds[3]))
                keys = ' '.join(['KEY_' + key for key in self._stickRegionBindings[region]])
                commands.append("stickzone action %s %s" % (region, keys))

        return '\n'.join(commands)
