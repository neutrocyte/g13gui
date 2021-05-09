#!/usr/bin/python

import unittest

import g13gui.model.bindings as bindings
from g13gui.model.bindingprofile import BindingProfile
from g13gui.observer.subject import ChangeType
from g13gui.observer.observer import ObserverTestCase


class PrefsTestCase(ObserverTestCase):
    def setUp(self):
        pass

    def testInitialSetup(self):
        bp = BindingProfile()
        self.assertEqual(bp.stickMode(), bindings.StickMode.KEYS)
        self.assertEqual(bp.stickRegions(), bindings.DEFAULT_STICK_REGIONS)
        self.assertEqual(bp.lcdColor(), bindings.DEFAULT_LCD_COLOR)
        self.assertEqual(bp._stickRegionBindings,
                         bindings.DEFAULT_STICK_REGION_BINDINGS)
        self.assertEqual(bp._keyBindings, bindings.DEFAULT_KEY_BINDINGS)
        self.assertEqual(bp._lcdColor, bindings.DEFAULT_LCD_COLOR)

    def testInvalidDict(self):
        bp = BindingProfile({})
        self.assertEqual(bp.stickMode(), bindings.StickMode.KEYS)
        self.assertEqual(bp.stickRegions(), bindings.DEFAULT_STICK_REGIONS)
        self.assertEqual(bp._stickRegionBindings,
                         bindings.DEFAULT_STICK_REGION_BINDINGS)
        self.assertEqual(bp._keyBindings, bindings.DEFAULT_KEY_BINDINGS)

    def testDictLoadSave(self):
        bp = BindingProfile()
        initial_d = bp.saveToDict()
        self.assertIsNotNone(initial_d)

        bp = BindingProfile(initial_d)
        new_d = bp.saveToDict()
        self.assertEqual(initial_d, new_d)

    def testBindKey(self):
        bp = BindingProfile()
        bp.registerObserver(self)

        bp.bindKey('G22', 'A')
        self.assertEqual(bp._keyBindings['G22'], 'A')
        self.assertEqual(bp.keyBinding('G22'), 'A')
        self.assertChangeCount(1)
        self.assertChangeNotified(bp, ChangeType.MODIFY, 'G22')
        self.assertChangeDataEquals('A')
        self.nextChange()

        bp.bindKey('STICK_UP', 'A')
        self.assertEqual(bp._stickRegionBindings['STICK_UP'], 'A')
        self.assertEqual(bp.keyBinding('STICK_UP'), 'A')
        self.assertChangeCount(1)
        self.assertChangeNotified(bp, ChangeType.MODIFY, 'STICK_UP')
        self.assertChangeDataEquals('A')
        self.nextChange()

    def testSetStickMode(self):
        bp = BindingProfile()
        bp.registerObserver(self)
        bp.setStickMode(bindings.StickMode.ABSOLUTE)
        self.assertEqual(bp._stickMode, bindings.StickMode.ABSOLUTE)
        self.assertEqual(bp.stickMode(), bindings.StickMode.ABSOLUTE)
        self.assertChangeCount(1)
        self.assertChangeNotified(bp, ChangeType.MODIFY, 'stickmode')
        self.assertChangeDataEquals(bindings.StickMode.ABSOLUTE)

        try:
            bp.setStickMode('zorch')
        except ValueError:
            pass
        else:
            self.fail('Expected ValueError from setStickMode')

    def testLCDColor(self):
        bp = BindingProfile()
        bp.registerObserver(self)
        bp.setLCDColor(1.0, 0.5, 0.1)
        self.assertEqual(bp._lcdColor, (1.0, 0.5, 0.1))
        self.assertEqual(bp.lcdColor(), (1.0, 0.5, 0.1))
        self.assertChangeCount(1)
        self.assertChangeNotified(bp, ChangeType.MODIFY, 'lcdcolor')
        self.assertChangeDataEquals((1.0, 0.5, 0.1))

    def testToCommandString(self):
        bp = BindingProfile()
        result = bp.toCommandString()
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
