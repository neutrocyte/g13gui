import enum

from builtins import property
from g13gui.bitwidgets.widget import Widget
from g13gui.bitwidgets.fonts import Fonts
from g13gui.bitwidgets.fonts import FontManager
from g13gui.observer.subject import ChangeType


class Alignment(enum.Enum):
    LEFT = 'left'
    CENTER = 'center'
    RIGHT = 'right'


class Label(Widget):
    def __init__(self, x, y, text,
                 font=Fonts.MEDIUM,
                 fill=True,
                 spacing=4,
                 align=Alignment.LEFT,
                 strokeWidth=0):
        Widget.__init__(self)
        self._position = (x, y)
        self._text = text
        self._font = font
        self._fill = fill
        self._spacing = spacing
        self._align = align
        self._strokeWidth = strokeWidth
        self._bounds = FontManager.getFont(self.font).getsize(self.text)

    def draw(self, ctx):
        if self._visible:
            ctx.text(self.position, self.text,
                     font=FontManager.getFont(self.font),
                     fill=self.fill,
                     spacing=self.spacing,
                     align=self.align.value,
                     stroke_width=self.strokeWidth)

    @property
    def text(self):
        return self._text

    @property
    def font(self):
        return self._font

    @property
    def spacing(self):
        return self._spacing

    @property
    def align(self):
        return self._align

    @property
    def strokeWidth(self):
        return self._strokeWidth

    @text.setter
    def text(self, text):
        self.setProperty('text', text)
        self.bounds = FontManager.getFont(self.font).getsize(self.text)

    @font.setter
    def font(self, font):
        self.setProperty('font', font)
        self.bounds = FontManager.getFont(self.font).getsize(self.text)

    @spacing.setter
    def spacing(self, spacing):
        self.setProperty('spacing', spacing)
        self.bounds = FontManager.getFont(self.font).getsize(self.text)

    @align.setter
    def align(self, align):
        self.setProperty('align', align)

    @strokeWidth.setter
    def strokeWidth(self, strokeWidth):
        self.setProperty('strokeWidth', strokeWidth)
