import gi
import queue

from g13gui.observer import Observer

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject


class GObjectObserverProxy(GObject.Object):
    def __init__(self, owner):
        GObject.Object.__init__(self)
        self._owner = owner

    @GObject.Signal(name='subject-changed')
    def subjectChanged(self):
        self._owner._gtkSubjectChanged(self)


class GtkObserver(Observer):
    def __init__(self):
        """Constructor. Must be called by a subclass' constructor."""
        self._observerQueue = queue.Queue()
        self._gobjectProxy = GObjectObserverProxy(self)

    def onSubjectChanged(self, subject, changeType, key, data=None):
        """Original Observer signal handler.

        Runs on a (possibly) background thread to put the notification into a
        queue, then signal to trampoline to the UI thread before handling the
        notification.
        """
        self._observerQueue.put((subject, changeType, key, data))
        self._gobjectProxy.emit("subject-changed")

    def _gtkSubjectChanged(self, widget):
        """GObject 'subject-changed' signal handler.

        Runs on the UI thread, and pops the change notification off the queue
        and processes it by way of the gtkSubjectChanged method that must be
        overridden.
        """
        (subject, changeType, key, data) = self._observerQueue.get()
        Observer.onSubjectChanged(self, subject, changeType, key, data)
        self._observerQueue.task_done()
