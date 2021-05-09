from builtins import property

from g13gui.bitwidgets.displaydevice import DisplayDevice
from g13gui.g13.displaydevice import G13DisplayDevice


class LoopbackDisplayDevice(G13DisplayDevice):
    """A loopback display device for the G13 manager.

    This one differs from the built-in G13DisplayDevice by preventing a direct
    write to the G13Manager's setLCDbuffer. This is specifically designed for
    the Applet use case, where the methods return LCD frames, rather than write
    directly.
    """

    def __init__(self):
        pass

    @property
    def frame(self):
        return self._frame

    def _pushFrame(self, lpbm):
        self._frame = lpbm
