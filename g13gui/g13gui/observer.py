#!/usr/bin/python

import unittest

from enum import Enum


class ChangeType(Enum):
    ADD = 0
    REMOVE = 1
    MODIFY = 2


class Observer(object):
    """Simple interface class to handle Observer-style notifications"""

    def onSubjectChanged(self, subject, changeType, key, data=None):
        """Event handler for observer notifications.

        Each subclass of Observer MUST override this method. There is no default
        method for handling events of this nature.

        subject[object]: the subject object that sent the event notifying something
          changed in its data model.
        changeType[ChangeType]: the type of change that occurred.
        key[string]: a required name for what field changed.
        data[object]: an optional context-dependent object, dict, or
          None, specifying what changed. In the case of an ADD or MODIFY,
          whatChanged should be the new data. In the case of a DELETE, it should
          be the old data (or None).
        """
        raise NotImplementedError(
            "%s did not override Observer#onSubjectChanged!" % (type(self)))


class Subject(object):
    """Simple class to handle the subject-side of the Observer pattern."""

    def registerObserver(self, observer):
        """Registers an Observer class as an observer of this object"""
        if '_observers' not in self.__dict__:
            self._observers = {observer}
        else:
            self._observers.add(observer)

    def removeObserver(self, observer):
        """Removes an observer from this object"""
        if '_observers' in self.__dict__:
            if observer in self._observers:
                self._observers.discard(observer)

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
            for observer in self._observers:
                for change in self._changes:
                    observer.onSubjectChanged(self, *change)
        self._changes = []


class ObserverTestCase(Observer, unittest.TestCase):
    def __init__(self, methodName):
        unittest.TestCase.__init__(self, methodName)
        self.changes = []
        self.clearChanges()

    def onSubjectChanged(self, subject, type, key, data=None):
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
