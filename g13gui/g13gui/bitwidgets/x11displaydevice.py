import PIL
import threading
import queue
from Xlib import X, display, Xutil
from builtins import property

from g13gui.bitwidgets.displaydevice import DisplayDevice


class X11DisplayDevice(DisplayDevice, threading.Thread):
    def __init__(self, name="BitWidgets"):
        threading.Thread.__init__(self, daemon=True)
        self._queue = queue.Queue()
        self._running = False
        self._name = name

    def run(self):
        self._display = display.Display()
        self.createWindow()
        self._running = True

        while self._running:
            while self._display.pending_events():
                self._display.next_event()

            image = self._queue.get()
            if image is None:
                self._running = False
                self._display.close()
                return

            points = []
            for x in range(0, 160):
                for y in range(0, 48):
                    if image.getpixel((x, y)) == 1:
                        points.append((x, y))

            self._win.fill_rectangle(self._inversegc, 0, 0, 160, 48)
            self._win.poly_point(self._gc, X.CoordModeOrigin, points)

    def createWindow(self):
        self._screen = self._display.screen()
        self._win = self._screen.root.create_window(
            0, 0, 160, 48, 2,
            self._screen.root_depth,
            X.InputOutput,
            X.CopyFromParent,
            background_pixel=self._screen.black_pixel,
            event_mask=(X.ExposureMask | X.StructureNotifyMask),
            colormap=X.CopyFromParent)
        self._gc = self._win.create_gc(
            foreground=self._screen.white_pixel,
            background=self._screen.black_pixel)
        self._inversegc = self._win.create_gc(
            foreground=self._screen.black_pixel,
            background=self._screen.white_pixel)

        self._win.set_wm_name(self._name)
        self._win.set_wm_icon_name(self._name)
        self._win.set_wm_class('bitwidgets', self._name)
        self._win.set_wm_normal_hints(
            flags=(Xutil.PPosition | Xutil.PSize | Xutil.PMinSize),
            min_width=160,
            min_height=48)
        self._win.map()

    @property
    def dimensions(self):
        return (160, 48)

    def update(self, image):
        if not self._running:
            raise RuntimeError('X11DisplayDevice is not running -- '
                               'cannot update.')

        self._queue.put(image)

    def shutdown(self):
        self._queue.put(None)
