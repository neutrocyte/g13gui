#!/usr/bin/python

import unittest
import observer


class TestIncorrectObserver(observer.Observer):
    pass


class TestSubject(observer.Subject):
    pass


class ObserverTestCase(observer.ObserverTestCase):
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
        self.subject.addChange(observer.ChangeType.ADD, 'foo')
        self.subject.registerObserver(testObserver)

        try:
            self.subject.notifyChanged()
        except NotImplementedError:
            pass
        else:
            unittest.fail('Expected NotImplementedError')

    def testSubclassNotification(self):
        self.subject.registerObserver(self)

        self.subject.addChange(observer.ChangeType.ADD, 'foo', 'bar')
        self.subject.notifyChanged()

        self.assertChangeCount(1)
        self.assertChangeNotified(self.subject, observer.ChangeType.ADD, 'foo')
        self.assertChangeDataEquals('bar')


if __name__ == '__main__':
    unittest.main()
