#!/usr/bin/python

import unittest
import g13gui.model.prefs as prefs

from g13gui.common import VERSION
from g13gui.observer import ChangeType
from g13gui.observer import ObserverTestCase


class PrefsTestCase(ObserverTestCase):
    def setUp(self):
        self.prefs = prefs.Preferences()
        self.prefs.registerObserver(self)

    def testInitialSetup(self):
        self.assertEqual(len(self.prefs.profiles()), 1)
        self.assertEqual(len(self.prefs.profileNames()), 1)
        self.assertEqual(self.prefs.selectedProfile(),
                         self.prefs.profiles()[prefs.DEFAULT_PROFILE_NAME])
        self.assertEqual(self.prefs.selectedProfileName(),
                         self.prefs.profileNames()[0])

    def testInitialDefaultProfile(self):
        self.prefs.initDefaultProfile()
        self.assertChangeCount(2)
        self.assertChangeNotified(self.prefs, ChangeType.ADD, 'profile')
        self.nextChange()
        self.assertChangeNotified(self.prefs, ChangeType.MODIFY,
                                  'selectedProfile')
        self.nextChange()

    def testAddRemoveProfile(self):
        self.prefs.addProfile('test', {})
        self.assertChangeCount(1)
        self.assertChangeNotified(self.prefs, ChangeType.ADD, 'profile')
        self.assertChangeDataEquals({'test': {}})
        self.nextChange()

        try:
            self.prefs.addProfile('test', {})
        except KeyError:
            pass
        else:
            self.fail('Expected duplicate names to throw KeyError on add.')

        self.prefs.removeProfile('test')
        self.assertChangeCount(1)
        self.assertChangeNotified(self.prefs, ChangeType.REMOVE, 'profile')
        self.assertChangeDataEquals('test')
        self.nextChange()

        self.prefs.removeProfile(prefs.DEFAULT_PROFILE_NAME)
        self.assertChangeCount(3)
        self.assertChangeNotified(self.prefs, ChangeType.REMOVE, 'profile')
        self.assertIsNotNone(self.getChangeData())
        self.nextChange()
        self.assertChangeNotified(self.prefs, ChangeType.ADD, 'profile')
        self.assertIsNotNone(self.getChangeData())
        self.nextChange()
        self.assertChangeNotified(self.prefs, ChangeType.MODIFY,
                                  'selectedProfile')
        self.assertChangeDataEquals(prefs.DEFAULT_PROFILE_NAME)
        self.nextChange()

        self.assertEqual(len(self.prefs.profiles()), 1)
        self.assertEqual(self.prefs.profileNames()[0],
                         prefs.DEFAULT_PROFILE_NAME)

    def testSetSelectedProfile(self):
        self.prefs.addProfile('test', {})
        self.skipChange()

        try:
            self.prefs.setSelectedProfile('doesntexist')
        except KeyError:
            pass
        else:
            self.fail('Expected setSelectedProfile with a bad profile '
                      'name to raise KeyError')

        self.prefs.setSelectedProfile('test')
        self.assertChangeCount(1)
        self.assertChangeNotified(self.prefs, ChangeType.MODIFY,
                                  'selectedProfile')
        self.assertChangeDataEquals('test')
        self.assertEqual(self.prefs.selectedProfileName(), 'test')
        self.assertEqual(self.prefs.selectedProfile(), {})

    def testSaveLoad(self):
        p = prefs.Preferences()
        initial_d = p.saveToDict()
        self.assertIsNotNone(initial_d)

        self.assertEqual(initial_d['version'], VERSION)
        self.assertIn('profiles', initial_d)
        self.assertIn('selectedProfile', initial_d)
        self.assertEqual('Default Profile', initial_d['selectedProfile'])

        p = prefs.Preferences(initial_d)
        new_d = p.saveToDict()
        self.assertEqual(initial_d, new_d)
        self.assertChangeCount(0)


if __name__ == '__main__':
    unittest.main()
