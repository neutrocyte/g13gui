from builtins import property

from g13gui.bitwidgets.widget import Widget
from g13gui.bitwidgets.glyph import Glyph
from g13gui.bitwidgets.rectangle import Rectangle
from g13gui.observer.subject import ChangeType


class Button(Widget):
    def __init__(self, glyph, fill=True):
        Widget.__init__(self)
        self._rect = Rectangle(*self.position, *self.bounds, fill=False)
        self._rect.show()
        self.addChild(self._rect)

        self._glyph = Glyph(*self.position, glyph=glyph)
        self._glyph.fill = fill
        self._glyph.show()
        self.addChild(self._glyph)

        self.pressed = False
        self.fill = fill

        self.registerObserver(self)
        self.changeTrigger(self._updatePositionAndBounds,
                           changeType=ChangeType.MODIFY,
                           keys={'position', 'bounds'})
        self.changeTrigger(self._updateStates,
                           changeType=ChangeType.MODIFY,
                           keys={'pressed'})

    def _updatePositionAndBounds(self, subject, changeType, key, data):
        self._rect.position = self.position
        self._rect.bounds = self.bounds

        (x, y) = self.position
        (w, h) = self.bounds
        (glyphW, glyphH) = self._glyph.bounds
        glyphX = x + (w // 2) - (glyphW // 2)
        glyphY = y + (h // 2) - (glyphH // 2)

        self._glyph.position = (glyphX, glyphY)

    def _updateStates(self, subject, changeType, key, data):
        self._rect.fill = self.pressed
        self._glyph.fill = not self.pressed

    @property
    def pressed(self):
        return self._pressed

    @pressed.setter
    def pressed(self, pressed):
        self.setProperty('pressed', pressed)

    @property
    def glyph(self):
        return self._glyph

    @glyph.setter
    def glyph(self, glyph):
        self.setProperty('glyph', glyph)
