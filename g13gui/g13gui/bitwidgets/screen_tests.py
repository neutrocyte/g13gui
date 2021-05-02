import unittest
import time

from g13gui.bitwidgets.display import Display
from g13gui.bitwidgets.x11displaydevice import X11DisplayDevice
from g13gui.bitwidgets.screen import Screen


class ScreenTests(unittest.TestCase):
    def setUp(self):
        self.dd = X11DisplayDevice(self.__class__.__name__)
        self.dd.start()
        time.sleep(0.25)
        self.d = Display(self.dd)
        self.s = Screen(self.d)

    def tearDown(self):
        time.sleep(1)
        self.dd.shutdown()
        self.dd.join()

    def testDraw(self):
        ctx = self.d.getContext()
        self.s.draw(ctx)
        self.d.commit()

    def testNextFrame(self):
        self.s.nextFrame()


if __name__ == '__main__':
    unittest.main()
