import gi
import time

from g13gui.applet.applet import Applet
from g13gui.applet.applet import RunApplet
from g13gui.bitwidgets.label import Label
from g13gui.bitwidgets.fonts import Fonts

gi.require_version('GLib', '2.0')
from gi.repository import GLib


class ClockApplet(Applet):
    NAME = 'Clock'

    def __init__(self):
        Applet.__init__(self, ClockApplet.NAME)

        self._timeLabel = Label(43, 8, '18:54:00', font=Fonts.LARGE)
        self._timeLabel.showAll()
        self.screen.addChild(self._timeLabel)

        self._updateTimeLabel()

    def _updateTimeLabel(self):
        (tm_year, tm_month, tm_mday, tm_hour,
         tm_min, tm_sec, tm_wday, tm_yday, tm_isdst) = time.localtime()
        self._timeLabel.text = '%d:%0.2d:%0.2d' % (tm_hour, tm_min, tm_sec)

    def _pushTime(self):
        self._updateTimeLabel()
        self.maybePresentScreen()
        return self.screen.visible

    def onShown(self, timestamp):
        self._updateTimeLabel()
        GLib.timeout_add_seconds(1, self._pushTime)


if __name__ == '__main__':
    RunApplet(ClockApplet)
