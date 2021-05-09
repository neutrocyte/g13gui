from builtins import property

from g13gui.bitwidgets.widget import Widget
from g13gui.bitwidgets.label import Label
from g13gui.bitwidgets.glyph import Glyph
from g13gui.bitwidgets.glyph import Glyphs
from g13gui.bitwidgets.rectangle import Rectangle
from g13gui.bitwidgets.fonts import Fonts
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


class LabelButton(Button):
    def __init__(self, text, isToggleable=False, hasMore=False, fill=True):
        Button.__init__(self, Glyphs.BLANK, fill)

        self._isOn = False
        self._isToggleable = isToggleable
        self._hasMore = hasMore

        self.removeChild(self._glyph)
        self._glyph = Label(*self.position, text, font=Fonts.TINY)
        self._glyph.show()
        self.addChild(self._glyph)

        self._moreGlyph = Glyph(0, 0, Glyphs.CHEVRON_RIGHT)
        self.addChild(self._moreGlyph)
        self._toggleGlyph = Glyph(0, 0, Glyphs.BOX)
        self.addChild(self._toggleGlyph)
        self.updateGlyphs()

    def updateGlyphs(self):
        if self.isOn:
            self._toggleGlyph.glyph = Glyphs.FILLED_BOX
        else:
            self._toggleGlyph.glyph = Glyphs.BOX

        self._moreGlyph.visible = self.hasMore
        self._toggleGlyph.visible = self.isToggleable

    def _updatePositionAndBounds(self, subject, changeType, key, data):
        super()._updatePositionAndBounds(subject, changeType, key, data)

        (x, y) = self.position
        (w, h) = self.bounds
        (glyphW, glyphH) = self._moreGlyph.bounds

        moreX = x + w - glyphW - 1
        moreY = y + (h // 2) - (glyphH // 2)
        self._moreGlyph.position = (moreX, moreY)

        toggleX = x + 1
        toggleY = y + (h // 2) - (glyphH // 2)
        self._toggleGlyph.position = (toggleX, toggleY)

        (labelX, labelY) = self._glyph.position
        labelY += 1
        self._glyph.position = (labelX, labelY)

    @property
    def isToggleable(self):
        return self._isToggleable

    @isToggleable.setter
    def isToggleable(self, value):
        self.setProperty('isToggleable', value)
        self.updateGlyphs()

    @property
    def isOn(self):
        return self._isOn

    @isOn.setter
    def isOn(self, value):
        self.setProperty('isOn', value)
        self.updateGlyphs()

    @property
    def isOff(self):
        return not self._isOn

    def toggle(self):
        self.setProperty('isOn', not self.isOn)
        self.updateGlyphs()

    @property
    def hasMore(self):
        return self._hasMore

    @hasMore.setter
    def hasMore(self, value):
        self.setProperty('hasMore', value)
        self.updateGlyphs()

    @property
    def text(self):
        return self._glyph.text

    @text.setter
    def text(self, text):
        self._glyph.text = text
