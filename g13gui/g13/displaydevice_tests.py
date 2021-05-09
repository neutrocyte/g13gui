import unittest
import time

from dbus.mainloop.glib import DBusGMainLoop

from g13gui.model.prefs import Preferences
from g13gui.bitwidgets.display import Display
from g13gui.bitwidgets.screen import Screen
from g13gui.bitwidgets.label import Label
from g13gui.bitwidgets.rectangle import Rectangle
from g13gui.g13.displaydevice import G13DisplayDevice
from g13gui.g13.manager import DeviceManager
from g13gui.bitwidgets import DISPLAY_WIDTH
from g13gui.bitwidgets import DISPLAY_HEIGHT


class DisplayDeviceTests(unittest.TestCase):
    def setUp(self):
        self.prefs = Preferences()
        self.manager = DeviceManager(self.prefs)
        self.manager.start()
        time.sleep(1)
        self.dd = G13DisplayDevice(self.manager)
        self.d = Display(self.dd)
        self.s = Screen(self.d)

    def tearDown(self):
        time.sleep(1)
        self.manager.shutdown()

    def testDisplay(self):
        rect = Rectangle(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        rect.show()
        self.s.addChild(rect)

        label = Label(0, 0, 'Hello, world!')
        label.show()
        self.s.addChild(label)

        self.s.buttonBar.hide()
        self.s.nextFrame()


if __name__ == '__main__':
    DBusGMainLoop(set_as_default=True)
    unittest.main()
