#!/usr/bin/python

import traceback

from builtins import property

from g13gui.common import VERSION
from g13gui.model.bindingprofile import BindingProfile
from g13gui.observer.subject import Subject
from g13gui.observer.subject import ChangeType


DEFAULT_PROFILE_NAME = 'Default Profile'


class Preferences(Subject):
    def __init__(self, dict=None):
        self._profiles = {}
        self._selectedProfile = None
        self._showWindowOnStart = True

        if dict:
            self.loadFromDict(dict)
        else:
            self.initDefaultProfile()

    @property
    def showWindowOnStart(self):
        return self._showWindowOnStart

    @showWindowOnStart.setter
    def showWindowOnStart(self, value):
        self.setProperty('showWindowOnStart', value)

    def profiles(self, profileName=None):
        if profileName:
            return self._profiles[profileName]
        return self._profiles

    def profileNames(self):
        return sorted(self._profiles.keys())

    def selectedProfile(self):
        return self._profiles[self._selectedProfile]

    def selectedProfileName(self):
        return self._selectedProfile

    def initDefaultProfile(self):
        self._initDefaultProfile()
        self.notifyChanged()

    def addProfile(self, name, profile):
        self._addProfile(name, profile)
        self.notifyChanged()

    def removeProfile(self, name):
        self._removeProfile(name)
        self.notifyChanged()

    def setSelectedProfile(self, name):
        self._setSelectedProfile(name)
        self.notifyChanged()

    def _initDefaultProfile(self):
        default_profile = BindingProfile()
        self._profiles = {DEFAULT_PROFILE_NAME: default_profile}
        self._selectedProfile = DEFAULT_PROFILE_NAME

        self.addChange(ChangeType.ADD, 'profile', {self.selectedProfileName(): self.selectedProfile()}),
        self.addChange(ChangeType.MODIFY, 'selectedProfile', self._selectedProfile)

    def _addProfile(self, name, profile):
        if name in self._profiles.keys():
            raise KeyError('Profile by name %s is already present' % name)
        self._profiles[name] = profile
        self.addChange(ChangeType.ADD, 'profile', {name: profile})

    def _removeProfile(self, name):
        del(self._profiles[name])
        self.addChange(ChangeType.REMOVE, 'profile', name)

        if len(self._profiles) == 0:
            self.initDefaultProfile()
        else:
            if self._selectedProfile == name:
                self.setSelectedProfile(sorted(self._profiles.keys())[0])

    def _setSelectedProfile(self, name):
        if name not in self._profiles.keys():
            raise KeyError('No profile by name %s present' % name)
        self._selectedProfile = name
        self.addChange(ChangeType.MODIFY, 'selectedProfile',
                       self._selectedProfile)

    def saveToDict(self):
        return {
            'version': VERSION,
            'showWindowOnStart': self._showWindowOnStart,
            'profiles': dict([(name, profile.saveToDict()) for name, profile in self._profiles.items()]),
            'selectedProfile': self._selectedProfile
        }

    def loadFromDict(self, dict):
        if dict['version'] != VERSION:
            print('WARNING: This profile config is from a different version '
                  '(wanted %s got %s)!' % (VERSION, dict['version']))
            print('This configuration may not load properly!')

        try:
            for name, profile in dict['profiles'].items():
                self._addProfile(name, BindingProfile(profile))

            self._setSelectedProfile(dict['selectedProfile'])
            self._showWindowOnStart = dict['showWindowOnStart']

        except (Exception) as err:
            print('Unable to initialize from dict: %s' % err)
            print('Continuing with defaults.')
            traceback.print_exc()

            self.initDefaultProfile()

        finally:
            self.clearChanges()
