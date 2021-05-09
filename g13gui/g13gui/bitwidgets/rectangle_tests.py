import unittest
import time

from g13gui.bitwidgets import DISPLAY_WIDTH
from g13gui.bitwidgets import DISPLAY_HEIGHT
from g13gui.bitwidgets.display import Display
from g13gui.bitwidgets.x11displaydevice import X11DisplayDevice
from g13gui.bitwidgets.screen import Screen
from g13gui.bitwidgets.rectangle import Rectangle


class RectangleTests(unittest.TestCase):
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

    def testRect(self):
        self.dd.name = 'testRect'
        ctx = self.display.getContext()
        rect = Rectangle(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT - 1, fill=True)
        rect.show()
        rect.draw(ctx)

        self.display.commit()


if __name__ == '__main__':
    unittest.main()
