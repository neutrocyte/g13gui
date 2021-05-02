import unittest
import time

from g13gui.model.prefs import Preferences
from g13gui.bitwidgets.display import Display
from g13gui.bitwidgets.screen import Screen
from g13gui.bitwidgets.label import Label
from g13gui.g13.displaydevice import G13DisplayDevice
from g13gui.g13.manager import Manager


class DisplayDeviceTests(unittest.TestCase):
    def setUp(self):
        self.prefs = Preferences()
        self.manager = Manager(self.prefs)
        self.manager.start()
        time.sleep(0.25)
        self.dd = G13DisplayDevice(self.manager)
        self.d = Display(self.dd)
        self.s = Screen(self.d)

    def tearDown(self):
        time.sleep(1)
        self.manager.shutdown()

    def testDisplay(self):
        label = Label(0, 0, 'Hello, world!')
        label.show()
        self.s.addChild(label)
        self.s.nextFrame()


if __name__ == '__main__':
    unittest.main()
