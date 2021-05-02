#!/usr/bin/python

import unittest

from enum import Enum


class ChangeType(Enum):
    ADD = 0
    REMOVE = 1
    MODIFY = 2


class Subject(object):
    """Simple class to handle the subject-side of the Observer pattern."""

    AllKeys = ''

    def registerObserver(self, observer, subscribedKeys=AllKeys):
        """Registers an Observer class as an observer of this object"""
        if subscribedKeys != Subject.AllKeys:
            subscribedKeys = frozenset(subscribedKeys)
        if '_observers' not in self.__dict__:
            self._observers = {observer: subscribedKeys}
        else:
            self._observers[observer] = subscribedKeys

    def removeObserver(self, observer):
        """Removes an observer from this object"""
        if '_observers' in self.__dict__:
            if observer in self._observers:
                del self._observers[observer]

    def addChange(self, type, key, data=None):
        """Schedules a change notification for transmitting later.

        type[ChangeType]: the type of change that occurred.
        key[string]: a required name for what field changed.
        data[object]: an optional context-dependent object, dict, or
          None, specifying what changed. In the case of an ADD or MODIFY,
          whatChanged should be the new data. In the case of a DELETE, it should
          be the old data (or None).
        """
        if '_changes' not in self.__dict__:
            self._changes = [(type, key, data)]
        else:
            self._changes.append((type, key, data))

    def clearChanges(self):
        """Removes all scheduled changes from the change buffer."""
        self._changes = []

    def notifyChange(self):
        raise NotImplementedError('Use Subject.notifyChanged instead')

    def notifyChanged(self):
        """Notifies all observers of scheduled changes in the change buffer.

        This method actually does the work of iterating through all observers
        and all changes and delivering them to the Observer's onSubjectChanged
        method.

        It is safe to call this if there are no changes to send in the buffer,
        or there are no observers to send changes to. Note that calling this
        when no observers are registered will still flush the change buffer.
        """
        if '_observers' in self.__dict__ and '_changes' in self.__dict__:
            for observer, subscribedKeys in self._observers.items():
                for type, key, data in self._changes:
                    if subscribedKeys == Subject.AllKeys or key in subscribedKeys:
                        observer.onSubjectChanged(self, type, key, data)

        self._changes = []

    def setProperty(self, propertyName, value, notify=True):
        propertyName = '_' + propertyName
        self.__dict__[propertyName] = value
        self.addChange(ChangeType.MODIFY, propertyName, value)
        if notify:
            self.notifyChanged()


class Observer(object):
    def _makeChangeTriggerKeys(self, changeType, keys):
        result = []
        if keys != Subject.AllKeys:
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
            raise NotImplementedError(
                'onSubjectChanged(%s, %s, %s, %s) fired with no '
                'listeners registered!' %
                (subject, changeType, key, data))

        found = False
        triggers = (
            self._changeTriggers.get((None, Subject.AllKeys)),
            self._changeTriggers.get((changeType, Subject.AllKeys)),
            self._changeTriggers.get((None, key)),
            self._changeTriggers.get((changeType, key)))

        for trigger in triggers:
            if trigger:
                found = True
                trigger(subject, changeType, key, data)

        if not found:
            raise NotImplementedError(
                'onSubjectChanged(%s, %s, %s, %s) fired without a listener!'
                % (subject, changeType, key, data))


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
