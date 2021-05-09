import enum

from builtins import property

from g13gui.bitwidgets.widget import Widget


class Glyphs(enum.Enum):
    DOWN_ARROW = [(2, 0), (2, 4), (0, 2), (4, 2), (2, 4)]
    UP_ARROW = [(2, 4), (2, 0), (4, 2), (0, 2), (2, 0)]
    CHECKMARK = [(0, 3), (1, 4), (4, 1), (1, 4)]
    XMARK = [(0, 0), (4, 4), (2, 2), (4, 0), (0, 4)]
    CHEVRON_RIGHT = [(4, 2), (2, 0), (2, 4), (4, 2), (2, 2)]
    WRENCH = [(0, 4), (0, 3), (2, 1), (2, 0), (3, 0), (4, 1), (4, 2), (3, 2),
              (1, 4)]
    BOX = [(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)]
    FILLED_BOX = [(1, 1), (3, 1), (3, 3), (1, 3), (1, 1), (2, 2)]
    BLANK = []

    BOUNDS = (5, 5)

    def transformTo(self, offsetx, offsety):
        return [(offsetx + x, offsety + y) for (x, y) in self.value]


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
