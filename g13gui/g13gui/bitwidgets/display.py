from PIL import Image
from PIL.ImageDraw import ImageDraw
from g13gui.observer import Subject
from g13gui.observer import ChangeType


class DisplayMetrics(object):
    WIDTH_PIXELS = 160
    HEIGHT_PIXELS = 48


class Display(Subject):
    def __init__(self):
        self._context = None
        self._bitmap = Image.new(mode='1',
                                 size=(DisplayMetrics.WIDTH_PIXELS,
                                       DisplayMetrics.HEIGHT_PIXELS))

    def getContext(self):
        return ImageDraw.Draw(self._bitmap)

    def commit(self):
        # convert to LPBM
        # upload to G13
        #
        pass

    def debug(self):
        self._bitmap.show()
