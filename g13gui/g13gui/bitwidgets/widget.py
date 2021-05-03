from builtins import property

from g13gui.observer.subject import Subject
from g13gui.observer.subject import ChangeType
from g13gui.observer.observer import Observer


class Widget(Subject, Observer):
    def __init__(self):
        Subject.__init__(self)
        Observer.__init__(self)

        self._children = []
        self.parent = None
        self.visible = False
        self.valid = False
        self.position = (0, 0)
        self.bounds = (0, 0)
        self.fill = False

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, xy):
        if type(xy) != tuple or  \
           len(xy) != 2 or       \
           type(xy[0]) != int or \
           type(xy[1]) != int:
            raise ValueError('Position must be a tuple of length 2')
        self.setProperty('position', xy)

    @property
    def bounds(self):
        return self._bounds

    @bounds.setter
    def bounds(self, wh):
        if type(wh) != tuple or  \
           len(wh) != 2 or       \
           type(wh[0]) != int or \
           type(wh[1]) != int:
            raise ValueError('Position must be a tuple of length 2')
        self.setProperty('bounds', wh)

    @property
    def fill(self):
        return True if self._fill else False

    @fill.setter
    def fill(self, fill):
        fill = 1 if fill else 0
        self.setProperty('fill', fill)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self.setProperty('parent', parent)

    def addChild(self, child):
        self._children.append(child)
        child.parent = self
        child.registerObserver(self, 'valid')
        self.addChange(ChangeType.ADD, 'child', child)
        self.notifyChanged()

    def removeChild(self, child):
        child.removeObserver(self)
        self._children.remove(child)
        child.parent = None
        self.addChange(ChangeType.REMOVE, 'child', child)
        self.notifyChanged()

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, visible):
        self.setProperty('visible', visible)

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def showAll(self):
        for child in self._children:
            if child:
                child.show()
        self.visible = True

    def draw(self, ctx):
        if self.visible:
            for child in self._children:
                if child.visible:
                    child.draw(ctx)
