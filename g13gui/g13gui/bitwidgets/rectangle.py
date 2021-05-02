from g13gui.bitwidgets.widget import Widget


class Rectangle(Widget):
    def __init__(self, x, y, w, h, radius=0, fill=True):
        Widget.__init__(self)
        self.position = (x, y)
        self.bounds = (w, h)
        self.radius = radius
        self.fill = fill

    def draw(self, ctx):
        if self._visible:
            points = (self._position[0], self._position[1],
                      self._position[0] + self._bounds[0],
                      self._position[1] + self._bounds[1])
            ctx.rounded_rectangle(*points,
                                  radius=self._radius,
                                  fill=self._fill)

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._setProperty('radius', radius)
