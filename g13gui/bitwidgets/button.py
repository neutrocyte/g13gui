import enum

from builtins import property
from g13gui.bitwidgets import DISPLAY_WIDTH
from g13gui.bitwidgets import DISPLAY_HEIGHT
from g13gui.bitwidgets.widget import Widget
from g13gui.bitwidgets.rectangle import Rectangle
from g13gui.observer.subject import ChangeType


GLYPH_WIDTH = 5
GLYPH_HEIGHT = 5


class Glyphs(enum.Enum):
    DOWN_ARROW = [(2, 0), (2, 4), (0, 2), (4, 2), (2, 4)]
    UP_ARROW = [(2, 4), (2, 0), (4, 2), (0, 2), (2, 0)]
    CHECKMARK = [(0, 3), (1, 4), (4, 1), (1, 4)]
    XMARK = [(0, 0), (4, 4), (2, 2), (4, 0), (0, 4)]
    BLANK = []

    BOUNDS = (5, 5)

    def transformTo(self, offsetx, offsety):
        return [(offsetx + x, offsety + y) for (x, y) in self.value]


class ButtonBar(Widget):
    MAX_BUTTONS = 4
    TOP_LINE = 33

    def __init__(self):
        Widget.__init__(self)
        self._children = [None] * ButtonBar.MAX_BUTTONS
        self.position = (0, ButtonBar.TOP_LINE)
        self.bounds = (DISPLAY_WIDTH, DISPLAY_HEIGHT - ButtonBar.TOP_LINE)

    def _buttonBounds(self):
        width = (DISPLAY_WIDTH // ButtonBar.MAX_BUTTONS) - 2
        height = DISPLAY_HEIGHT - ButtonBar.TOP_LINE
        return (width, height)

    def _positionForSlot(self, buttonNum):
        slotWidth = DISPLAY_WIDTH / ButtonBar.MAX_BUTTONS
        slotX = (buttonNum * slotWidth)
        slotY = ButtonBar.TOP_LINE + 1
        return (int(slotX), int(slotY))

    def button(self, buttonNum):
        return self._children[buttonNum]

    def setButton(self, buttonNum, button):
        if self._children[buttonNum]:
            self.removeChild(self._children[buttonNum])

        self._children[buttonNum] = button
        button.position = self._positionForSlot(buttonNum)
        button.bounds = self._buttonBounds()
        button.parent = self

        self.addChange(ChangeType.ADD, 'child', button)
        self.notifyChanged()

    def addChild(self, button):
        buttonNum = self._children.index(None)
        if buttonNum > ButtonBar.MAX_BUTTONS:
            raise ValueError('Can\'t store another button!')
        self.setButton(buttonNum, button)

    def removeChild(self, button):
        buttonNum = self._children.index(button)
        button = self._children[buttonNum]
        self._children[buttonNum] = None
        button.parent = None

        self.addChange(ChangeType.REMOVE, 'child', button)
        self.notifyChanged()

    def draw(self, ctx):
        if self.visible:
            for child in self._children:
                if child and child.visible:
                    child.draw(ctx)

            # Top line
            ctx.line(self.position + (DISPLAY_WIDTH,
                                      ButtonBar.TOP_LINE),
                     fill=1)

            # Dividing lines
            for slot in range(0, ButtonBar.MAX_BUTTONS):
                (x, y) = self._positionForSlot(slot)
                x -= 1
                ctx.line((x, y) + (x, DISPLAY_HEIGHT),
                         fill=1)


class Glyph(Widget):
    def __init__(self, x, y, glyph=Glyphs.BLANK, fill=True):
        Widget.__init__(self)
        self.glyph = glyph
        self.position = (x, y)
        self.fill = fill

    @property
    def glyph(self):
        return self._glyph

    @glyph.setter
    def glyph(self, glyph):
        self.setProperty('glyph', glyph)

    @property
    def bounds(self):
        return Glyphs.BOUNDS.value

    def draw(self, ctx):
        if self.visible:
            (x, y) = self.position
            xformedGlyph = self.glyph.transformTo(x, y)
            ctx.line(xformedGlyph, fill=self._fill)


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
