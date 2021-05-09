import unittest
import time

from g13gui.bitwidgets.display import Display
from g13gui.bitwidgets.x11displaydevice import X11DisplayDevice
from g13gui.bitwidgets.screen import Screen
from g13gui.bitwidgets.listview import ListView


class ListViewTests(unittest.TestCase):
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

    def testEmptyList(self):
        lv = ListView([])
        lv.show()
        self.screen.addChild(lv)
        self.screen.nextFrame()

    def testFullLists(self):
        lv = ListView([
            'One',
            'Two',
            'Three'
        ])
        lv.show()
        self.screen.addChild(lv)
        self.screen.nextFrame()


if __name__ == '__main__':
    unittest.main()
