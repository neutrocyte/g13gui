import unittest

import PIL.Image

from g13gui.bitwidgets.display import LPBM_LENGTH
from g13gui.bitwidgets.display import ImageToLPBM
from g13gui.bitwidgets.fonts import Fonts
from g13gui.bitwidgets.fonts import FontManager
from g13gui.bitwidgets.display import Display
from g13gui.bitwidgets.display import DisplayMetrics


class DisplayTests(unittest.TestCase):
    def setUp(self):
        self.d = Display()

    def testConversion(self):
        ctx = self.d.getContext()
        ctx.rectangle((0, 0, 160, 43), fill=1)
        ctx.text((0, 0), "Hello world!",
                 font=FontManager.getFont(Fonts.HUGE), fill=0)
        result = ImageToLPBM(self.d._bitmap)

        self.assertEqual(len(result), LPBM_LENGTH)

        with open('/run/g13d/in', 'wb') as fp:
            fp.write(result)

if __name__ == '__main__':
    unittest.main()
