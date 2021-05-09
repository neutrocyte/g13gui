import unittest
import time

from g13gui.bitwidgets.display import Display
from g13gui.bitwidgets.x11displaydevice import X11DisplayDevice
from g13gui.bitwidgets.screen import Screen
from g13gui.bitwidgets.button import Button
from g13gui.bitwidgets.button import LabelButton
from g13gui.bitwidgets.glyph import Glyphs
from g13gui.bitwidgets.glyph import Glyph
from g13gui.bitwidgets.label import Label
from g13gui.bitwidgets.fonts import Fonts


class ButtonTests(unittest.TestCase):
    def setUp(self):
        self.dd = X11DisplayDevice(self.__class__.__name__)
        self.dd.start()
        time.sleep(0.25)
        self.display = Display(self.dd)
        self.screen = Screen(self.display)

    def tearDown(self):
        time.sleep(1)
        self.dd.shutdown()
        self.dd.join()

    def testGlyph(self):
        self.dd.name = 'testGlyph'
        ctx = self.display.getContext()
        glyph = Glyph(10, 10, Glyphs.CHECKMARK)
        glyph.fill = True
        glyph.show()
        glyph.draw(ctx)

        self.display.commit()

    def testExButton(self):
        self.dd.name = 'testExButton'
        ctx = self.display.getContext()
        exButton = Button(Glyphs.XMARK)
        exButton.show()
        exButton.draw(ctx)
        upButton = Button(Glyphs.UP_ARROW)
        upButton.position = (10, 0)
        upButton.show()
        upButton.draw(ctx)
        downButton = Button(Glyphs.DOWN_ARROW)
        downButton.position = (20, 0)
        downButton.show()
        downButton.draw(ctx)
        checkButton = Button(Glyphs.CHECKMARK)
        checkButton.position = (30, 0)
        checkButton.show()
        checkButton.draw(ctx)

        self.display.commit()

    def testButtonBar(self):
        self.dd.name = 'testButtonBar'
        exButton = Button(Glyphs.XMARK)
        upButton = Button(Glyphs.UP_ARROW)
        downButton = Button(Glyphs.DOWN_ARROW)
        checkButton = Button(Glyphs.CHECKMARK)

        self.screen.buttonBar.addChild(exButton)
        self.screen.buttonBar.addChild(upButton)
        self.screen.buttonBar.addChild(downButton)
        self.screen.buttonBar.addChild(checkButton)
        self.screen.buttonBar.showAll()

        self.screen.nextFrame()

    def testLabelButton(self):
        self.dd.name = 'testLabelButton'
        testButton = LabelButton("Test")
        self.screen.buttonBar.addChild(testButton)
        self.screen.buttonBar.showAll()
        self.screen.nextFrame()


if __name__ == '__main__':
    unittest.main()
