import time

from builtins import property
from g13gui.bitwidgets.widget import Widget
from g13gui.bitwidgets.button import ButtonBar


MIN_NSECS_BETWEEN_FRAMES = 125000


class Screen(Widget):
    def __init__(self, display):
        Widget.__init__(self)
        self._display = display
        self._buttonBar = ButtonBar()
        self._buttonBar.show()
        self.show()

    @property
    def buttonBar(self):
        return self._buttonBar

    def draw(self, ctx):
        Widget.draw(self, ctx)
        self._buttonBar.draw(ctx)

    def nextFrame(self):
        self._display.clear()
        ctx = self._display.getContext()
        self.draw(ctx)
        self._display.commit()
