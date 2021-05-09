import unittest
import time

from g13gui.bitwidgets.display import Display
from g13gui.bitwidgets.x11displaydevice import X11DisplayDevice
from g13gui.bitwidgets.label import Label


class LabelTests(unittest.TestCase):
    def setUp(self):
        self.dd = X11DisplayDevice(self.__class__.__name__)
        self.dd.start()
        time.sleep(0.25)
        self.d = Display(self.dd)

    def tearDown(self):
        time.sleep(1)
        self.dd.shutdown()
        self.dd.join()

    def testDraw(self):
        label = Label(0, 0, "Hello world!")
        ctx = self.d.getContext()
        label.show()
        label.draw(ctx)
        self.d.commit()


if __name__ == '__main__':
    unittest.main()
