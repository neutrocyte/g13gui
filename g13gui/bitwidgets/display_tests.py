import unittest
import time

from g13gui.bitwidgets.display import Display
from g13gui.bitwidgets.x11displaydevice import X11DisplayDevice


class DisplayTests(unittest.TestCase):
    def setUp(self):
        self.dd = X11DisplayDevice(self.__class__.__name__)
        self.dd.start()
        time.sleep(0.25)
        self.d = Display(self.dd)

    def tearDown(self):
        time.sleep(1)
        self.dd.shutdown()
        self.dd.join()

    def testUpdate(self):
        ctx = self.d.getContext()
        ctx.line((0, 0)+(160, 48), fill=1)
        ctx.line((160, 0)+(0, 48), fill=1)
        self.d.commit()


if __name__ == '__main__':
    unittest.main()
