#!/usr/bin/python

import unittest
import time

from g13gui.bitwidgets.fonts import Fonts
from g13gui.bitwidgets.fonts import FontManager
from g13gui.bitwidgets.display import Display
from g13gui.bitwidgets.x11displaydevice import X11DisplayDevice


class FontsTests(unittest.TestCase):
    def setUp(self):
        self.dd = X11DisplayDevice(self.__class__.__name__)
        self.dd.start()
        time.sleep(0.25)
        self.d = Display(self.dd)

    def tearDown(self):
        time.sleep(1)
        self.dd.shutdown()
        self.dd.join()

    def testFontDrawing(self):
        ctx = self.d.getContext()
        ctx.text((0, 0), "Hello world!",
                 font=FontManager.getFont(Fonts.TINY),
                 fill=(1))
        ctx.text((0, 6), "Hello world!",
                 font=FontManager.getFont(Fonts.SMALL),
                 fill=(1))
        ctx.text((0, 11), "Hello world!",
                 font=FontManager.getFont(Fonts.MEDIUM),
                 fill=(1))
        ctx.text((0, 19), "Hello world!",
                 font=FontManager.getFont(Fonts.LARGE),
                 fill=(1))
        ctx.text((0, 31), "Hello world!",
                 font=FontManager.getFont(Fonts.HUGE),
                 fill=(1))
        self.d.commit()


if __name__ == '__main__':
    unittest.main()
