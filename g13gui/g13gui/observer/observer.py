#!/usr/bin/python

import unittest

from enum import Enum

from g13gui.observer.subject import Subject


class Observer(object):
    def _makeChangeTriggerKeys(self, changeType, keys):
        result = []
        if keys != Subject.AllKeys:
            if type(keys) != set:
                keys = {keys}
            for key in keys:
                result.append((changeType, key))
        else:
            result.append((changeType, keys))

        return result

    def changeTrigger(self, callback,
                      changeType=None, keys=Subject.AllKeys):
        if '_changeTriggers' not in self.__dict__:
            self._changeTriggers = {}
        for key in self._makeChangeTriggerKeys(changeType, keys):
            self._changeTriggers[key] = callback

    def onSubjectChanged(self, subject, changeType, key, data=None):
        """Generic event handler dispatcher for observer notifications.

        Each subclass of Observer MUST call setChangeTrigger to register a
        callback method in its __init__.

        subject[object]: the subject object that sent the event notifying
          something changed in its data model.
        changeType[ChangeType]: the type of change that occurred.
        key[string]: a required name for what field changed.
        data[object]: an optional context-dependent object, dict, or
          None, specifying what changed. In the case of an ADD or MODIFY,
          whatChanged should be the new data. In the case of a DELETE, it
          should be the old data (or None).
        """
        if '_changeTriggers' not in self.__dict__:
            return

        triggers = (
            self._changeTriggers.get((None, Subject.AllKeys)),
            self._changeTriggers.get((changeType, Subject.AllKeys)),
            self._changeTriggers.get((None, key)),
            self._changeTriggers.get((changeType, key)))

        for trigger in triggers:
            if trigger:
                trigger(subject, changeType, key, data)


class ObserverTestCase(Observer, unittest.TestCase):
    def __init__(self, methodName):
        unittest.TestCase.__init__(self, methodName)
        self.changeTrigger(self.changed)
        self.clearChanges()

    def changed(self, subject, type, key, data=None):
        self.changes.insert(0, {
            'subject': subject,
            'type': type,
            'key': key,
            'data': data
        })

    def assertChangeCount(self, count):
        try:
            self.assertEqual(len(self.changes), count)
        except AssertionError as e:
            message = [repr(e), '']
            message.append('Changes were:')
            num = 1
            self.changes.reverse()
            for change in self.changes:
                message.append('%s: %s' % (num, repr(change)))
                num = num + 1
            raise AssertionError('\n'.join(message))

    def assertChangeNotified(self, subject, type, key):
        change = self.changes[-1]
        self.assertEqual(change['subject'], subject)
        self.assertEqual(change['type'], type)
        self.assertEqual(change['key'], key)

    def getChangeData(self):
        return self.changes[-1]['data']

    def assertChangeDataEquals(self, data):
        change = self.changes[-1]
        self.assertEqual(change['data'], data)

    def skipChange(self):
        self.nextChange()

    def nextChange(self):
        self.changes.pop()

    def clearChanges(self):
        self.changes = []
