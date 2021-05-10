from g13gui.bitwidgets.widget import Widget
from g13gui.bitwidgets.rectangle import Rectangle
from g13gui.bitwidgets.label import Label
from g13gui.bitwidgets.fonts import Fonts
from g13gui.bitwidgets import DISPLAY_WIDTH
from g13gui.bitwidgets import DISPLAY_HEIGHT


class Dialog(Widget):
    def __init__(self, text):
        Widget.__init__(self)

        self._text = text
        self._rect = Rectangle(0, 0, DISPLAY_WIDTH - 1, DISPLAY_HEIGHT - 1,
                               fill=False, outline=True, width=3)
        self._label = Label(0, 0, text, font=Fonts.LARGE)
        self.addChild(self._rect)
        self.addChild(self._label)

        self._updateLayout()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self.setProperty('text', value)
        self._label.text = value
        self._updateLayout()

    def _updateLayout(self):
        (w, h) = self._label.bounds
        x = ((DISPLAY_WIDTH - 1) // 2) - (w // 2)
        y = ((DISPLAY_HEIGHT - 1) // 2) - (h // 2)
        self._label.position = (x, y)
