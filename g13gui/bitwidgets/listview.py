from g13gui.bitwidgets.widget import Widget
from g13gui.bitwidgets.buttonbar import ButtonBar
from g13gui.bitwidgets.glyph import Glyph
from g13gui.bitwidgets.glyph import Glyphs
from g13gui.bitwidgets.rectangle import Rectangle
from g13gui.bitwidgets.label import Label
from g13gui.bitwidgets.fonts import Fonts
from g13gui.bitwidgets.fonts import FontManager
from g13gui.bitwidgets import DISPLAY_WIDTH
from g13gui.bitwidgets import DISPLAY_HEIGHT
from g13gui.observer.subject import ChangeType


class ListView(Widget):
    def __init__(self, model, markedIdx=None, font=Fonts.SMALL):
        Widget.__init__(self)
        self.model = model
        self._font = font

        self.position = (0, 0)
        self.bounds = (DISPLAY_WIDTH, ButtonBar.TOP_LINE - 1)

        self._markedIdx = markedIdx
        self._selectionIdx = 0
        self._visibilityOffset = 0

        self._setup()
        self.update()

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        self._model = sorted(list(model))

    @property
    def selectionIndex(self):
        return self._selectionIdx

    @selectionIndex.setter
    def selectionIndex(self, value):
        self._selectionIdx = value

    def selection(self):
        items = sorted(self._model)
        if self._selectionIdx >= len(items):
            return None
        return items[self._selectionIdx]

    def markedItem(self):
        items = sorted(self._model)
        if self._markedIdx >= len(items):
            return None
        return items[self._markedIdx]

    def nextSelection(self):
        maxIdx = len(self._model) - 1
        maxIdx = 0 if maxIdx < 0 else maxIdx
        idx = self.selectionIndex

        idx += 1

        if idx > maxIdx:
            idx = maxIdx

        maxVisibleItem = self._visibilityOffset + self._numVisibleItems - 1
        if idx > maxVisibleItem:
            self._visibilityOffset += 1

        self.selectionIndex = idx
        self.update()

    def prevSelection(self):
        idx = self.selectionIndex
        idx -= 1
        if idx < 0:
            idx = 0

        if idx < self._visibilityOffset:
            self._visibilityOffset -= 1

        self.selectionIndex = idx
        self.update()

    def markSelection(self):
        self._markedIdx = self.selectionIndex

    @property
    def markedIndex(self):
        return self._markedIdx

    @markedIndex.setter
    def markedIndex(self, value):
        self._markedIdx = value

    def update(self):
        items = sorted(self._model)
        startIdx = self._visibilityOffset
        endIdx = self._visibilityOffset + self._numVisibleItems
        maxItemIdx = len(items) - 1

        for idx in range(startIdx, endIdx):
            name = ''
            if idx <= maxItemIdx:
                name = items[idx]

            itemIdx = idx - startIdx
            item = self._items[itemIdx]
            item.text = name
            item.isSelected = (idx == self._markedIdx)
            item.isHighlighted = (idx == self.selectionIndex)

    def _setup(self):
        self._items = []

        li = ListItem(0, 'Wqpj', font=self._font)
        (_, self._liHeight) = li.bounds
        self._numVisibleItems = self._bounds[1] // self._liHeight

        for i in range(0, self._numVisibleItems):
            y = int(self._liHeight * i)
            li = ListItem(y, '', font=self._font)
            li.show()
            self.addChild(li)
            self._items.append(li)

        self._items[self.selectionIndex].isHighlighted = True


class ListItem(Widget):
    def __init__(self, ypos, text,
                 is_selected=False,
                 is_highlighted=False,
                 font=Fonts.SMALL):
        Widget.__init__(self)

        self._text = text
        self._isSelected = is_selected
        self._isHighlighted = is_highlighted

        self._font = font
        (_, self._fontHeight) = FontManager.getFont(self._font).getsize('Wqpj')

        self.position = (0, ypos)
        self.bounds = (DISPLAY_WIDTH, self._fontHeight + 3)

        self._setup()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self._label.text = text

    @property
    def isHighlighted(self):
        return self._isHighlighted

    @isHighlighted.setter
    def isHighlighted(self, is_highlighted):
        self._isHighlighted = is_highlighted
        self._updateStates()

    @property
    def isSelected(self):
        return self._isSelected

    @isSelected.setter
    def isSelected(self, is_selected):
        self._isSelected = is_selected
        self._updateStates()

    def _updateStates(self):
        self._rect.fill = self.isHighlighted
        self._label.fill = not self.isHighlighted

        self._indicator.fill = self.isHighlighted ^ self.isSelected

    def _setup(self):
        self._rect = Rectangle(*self.position, *self.bounds,
                               fill=self.isHighlighted)
        self._rect.show()
        self.addChild(self._rect)

        self._indicator = Glyph(*self.position, Glyphs.CHECKMARK)
        self._indicator.position = (2, (self.position[1] + self._fontHeight // 2) - 1)
        self._indicator.show()
        self.addChild(self._indicator)

        self._label = Label(10, self.position[1] + 2, self._text,
                            fill=not self.isHighlighted, font=self._font)
        self._label.show()
        self.addChild(self._label)

        self._updateStates()
