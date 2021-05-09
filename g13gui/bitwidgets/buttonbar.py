from g13gui.observer.subject import ChangeType
from g13gui.bitwidgets import DISPLAY_WIDTH
from g13gui.bitwidgets import DISPLAY_HEIGHT
from g13gui.bitwidgets.widget import Widget


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
