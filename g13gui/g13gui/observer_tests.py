#!/usr/bin/python

import unittest
import observer

class TestObserver(observer.Observer):
    def __init__(self):
        self.changes = []

    def onSubjectChanged(self, subject, type, key, whatChanged):
        self.changes.insert(0, {
            'subject': subject,
            'type': type,
            'key': key,
            'whatChanged': whatChanged
        })

    def assertChangeNotified(self, subject, type, key):
        change = self.changes.pop()
        assert(change['subject'] == subject)
        assert(change['type'] == type)
        assert(change['key'] == key)
        return change['whatChanged']


class TestIncorrectObserver(observer.Observer):
    pass


class TestSubject(observer.Subject):
    pass


class ObserverTestCase(unittest.TestCase):
    def setUp(self):
        self.subject = TestSubject()

    def testRegistration(self):
        observer = TestObserver()
        self.subject.registerObserver(observer)
        assert(len(self.subject._observers) == 1)

        self.subject.registerObserver(observer)
        assert(len(self.subject._observers) == 1)

        self.subject.removeObserver(observer)
        assert(len(self.subject._observers) == 0)

        self.subject.removeObserver(observer)

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
        o = TestObserver()
        self.subject.registerObserver(o)

        self.subject.addChange(observer.ChangeType.ADD, 'foo', 'bar')
        self.subject.notifyChanged()

        result = o.assertChangeNotified(
            self.subject, observer.ChangeType.ADD, 'foo')
        assert(result == 'bar')


if __name__ == '__main__':
    unittest.main()
