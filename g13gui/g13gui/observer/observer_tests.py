#!/usr/bin/python

import unittest

from builtins import property

from g13gui.observer.observer import Observer
from g13gui.observer.observer import ObserverTestCase
from g13gui.observer.subject import Subject
from g13gui.observer.subject import ChangeType


class TestIncorrectObserver(Observer):
    def __hash__(self):
        return hash('TestIncorrectObserver')


class TestSubject(Subject):
    def __init__(self):
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.setProperty('value', value)


class ObserverTestCase(ObserverTestCase):
    def setUp(self):
        self.subject = TestSubject()

    def testRegistration(self):
        self.subject.registerObserver(self)
        self.assertEqual(len(self.subject._observers), 1)

        self.subject.registerObserver(self)
        self.assertEqual(len(self.subject._observers), 1)

        self.subject.removeObserver(self)
        self.assertEqual(len(self.subject._observers), 0)

        self.subject.removeObserver(self)

    def testSubclassNotificationError(self):
        testObserver = TestIncorrectObserver()
        self.subject.addChange(ChangeType.ADD, 'foo')
        self.subject.registerObserver(testObserver)

        try:
            self.subject.notifyChanged()
        except NotImplementedError:
            pass
        else:
            unittest.fail('Expected NotImplementedError')

    def testSubclassNotification(self):
        self.subject.registerObserver(self)

        self.subject.addChange(ChangeType.ADD, 'foo', 'bar')
        self.subject.notifyChanged()

        self.assertChangeCount(1)
        self.assertChangeNotified(self.subject, ChangeType.ADD, 'foo')
        self.assertChangeDataEquals('bar')

    def testSubscribedKeys(self):
        self.subject.registerObserver(self, {'a', 'b'})

        self.subject.addChange(ChangeType.ADD, 'a')
        self.subject.addChange(ChangeType.ADD, 'b')
        self.subject.addChange(ChangeType.ADD, 'c')
        self.subject.notifyChanged()

        self.assertChangeCount(2)
        self.assertChangeNotified(self.subject, ChangeType.ADD, 'a')
        self.nextChange()
        self.assertChangeNotified(self.subject, ChangeType.ADD, 'b')
        self.nextChange()


if __name__ == '__main__':
    unittest.main()
