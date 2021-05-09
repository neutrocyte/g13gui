import enum


class ChangeType(enum.Enum):
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
        realPropertyName = '_' + propertyName
        self.__dict__[realPropertyName] = value
        self.addChange(ChangeType.MODIFY, propertyName, value)
        if notify:
            self.notifyChanged()
