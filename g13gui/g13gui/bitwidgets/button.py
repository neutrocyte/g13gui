import enum

from builtins import property
from g13gui.bitwidgets import DISPLAY_WIDTH
from g13gui.bitwidgets import DISPLAY_HEIGHT
from g13gui.bitwidgets.widget import Widget
from g13gui.observer.subject import ChangeType


GLYPH_WIDTH = 5
GLYPH_HEIGHT = 5


class Glyphs(enum.Enum):
    DOWN_ARROW = [(2, 0), (2, 4), (0, 2), (4, 2), (2, 4)]
    UP_ARROW = [(2, 4), (2, 0), (4, 2), (0, 2), (2, 0)]
    CHECKMARK = [(0, 3), (1, 4), (4, 1), (1, 4)]
    XMARK = [(0, 0), (4, 4), (2, 2), (4, 0), (0, 4)]

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

    def button(self, buttonNum):
        return self._children[buttonNum]

    def setButton(self, buttonNum, button):
        if self._children[buttonNum]:
            self.removeChild(self._children[buttonNum])

        self._children[buttonNum] = button
        position = self._positionForButton(buttonNum)
        button.position = position
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

    def _positionForSlot(self, buttonNum):
        slotWidth = DISPLAY_WIDTH / ButtonBar.MAX_BUTTONS
        slotX = (buttonNum * slotWidth)
        slotY = ButtonBar.TOP_LINE + 2

        return (slotX, slotY)

    def _positionForButton(self, buttonNum):
        (slotX, slotY) = self._positionForSlot(buttonNum)
        slotWidth = DISPLAY_WIDTH / ButtonBar.MAX_BUTTONS
        slotHeight = DISPLAY_HEIGHT - ButtonBar.TOP_LINE - 2

        (width, height) = self._children[buttonNum].bounds
        x_pos = int(slotX + (slotWidth / 2) - (width / 2))
        y_pos = int(slotY + (slotHeight / 2) - (height / 2))

        return (x_pos, y_pos)

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
                position = list(self._positionForSlot(slot))
                position[0] -= 2
                ctx.line(tuple(position) + (position[0], DISPLAY_HEIGHT),
                         fill=1)


class Button(Widget):
    def __init__(self, glyph, fill=True):
        Widget.__init__(self)
        self.glyph = glyph
        self.fill = fill
        self.bounds = (5, 5)

    def draw(self, ctx):
        if self._visible:
            xformedGlyph = self._glyph.transformTo(*self._position)
            ctx.line(xformedGlyph, fill=self.fill)

    @property
    def glyph(self):
        return self._glyph

    @glyph.setter
    def glyph(self, glyph):
        self.setProperty('glyph', glyph)
