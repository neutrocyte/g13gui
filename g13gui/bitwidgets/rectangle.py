from g13gui.bitwidgets.widget import Widget


class Rectangle(Widget):
    def __init__(self, x, y, w, h, fill=True, outline=0):
        Widget.__init__(self)
        self.position = (x, y)
        self.bounds = (w, h)
        self.fill = fill
        self._outline = outline

    @property
    def outline(self):
        return self._outline

    @outline.setter
    def outline(self, value):
        self.setAttribute('outline', value)

    def draw(self, ctx):
        if self._visible:
            points = (self._position[0], self._position[1],
                      self._position[0] + self._bounds[0],
                      self._position[1] + self._bounds[1])
            ctx.rectangle(points,
                          fill=self._fill,
                          outline=self._outline)
