from builtins import property

from g13gui.bitwidgets.widget import Widget
from g13gui.bitwidgets.rectangle import Rectangle


class Graph(Widget):
    def __init__(self, x, y, w, h):
        Widget.__init__(self)

        self._rect = Rectangle(x, y, w, h, fill=True)
        self.addChild(self._rect)

        self.position = (x, y)
        self.bounds = (w, h)

        self._timeseries = [0] * w

    def addValue(self, value):
        if value > 1 or value < 0:
            value = 0

        (w, h) = self.bounds
        self._timeseries.append(value)
        if len(self._timeseries) > w:
            del self._timeseries[0]

    @property
    def bounds(self):
        return self._bounds

    @bounds.setter
    def bounds(self, wh):
        self.setProperty('bounds', wh)
        self._rect.bounds = wh
        self._timeseries = [0] * wh[0]

    def draw(self, ctx):
        super().draw(ctx)

        (x, y) = self.position
        (w, h) = self.bounds
        (t, b, l, r) = (y, y + h, x, x + w)
        tl = (l, t)
        bl = (l, b)
        br = (r, b)

        if self.visible:
            ctx.line(tl+bl, fill=1)
            ctx.line(bl+br, fill=1)

            for idx, value in enumerate(self._timeseries):
                xoffs = idx + x
                scaledValue = int(value * h)
                yoffs = b - scaledValue

                points = (xoffs, yoffs,
                          xoffs, b)
                ctx.line(points, fill=1)
