from g13gui.bitwidgets.widget import Widget


class Rectangle(Widget):
    def __init__(self, x, y, w, h, fill=True, outline=False, width=1):
        Widget.__init__(self)
        self.position = (x, y)
        self.bounds = (w, h)
        self.fill = fill
        self.outline = outline
        self.width = width

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self.setProperty('width', width)

    @property
    def outline(self):
        return True if self._outline else False

    @outline.setter
    def outline(self, value):
        value = 1 if value else 0
        self.setProperty('outline', value)

    def draw(self, ctx):
        if self._visible:
            points = (self._position[0], self._position[1],
                      self._position[0] + self._bounds[0],
                      self._position[1] + self._bounds[1])
            ctx.rectangle(points,
                          fill=self._fill,
                          outline=self._outline,
                          width=self._width)
