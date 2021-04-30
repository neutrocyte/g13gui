import struct
import PIL.ImageDraw
import PIL.PyAccess
import sys
from io import BytesIO
from PIL import Image
from g13gui.observer import Subject
from g13gui.observer import ChangeType


class DisplayMetrics(object):
    WIDTH_PIXELS = 160
    HEIGHT_PIXELS = 48


LPBM_LENGTH = 960


def ImageToLPBM(image):
    i = PIL.PyAccess.new(image, readonly=True)
    bio = BytesIO()

    maxBytes = (DisplayMetrics.WIDTH_PIXELS * DisplayMetrics.HEIGHT_PIXELS // 8)
    row = 0
    col = 0

    for byteNum in range(0, maxBytes):
        b = int()

        if row == 40:
            maxSubrow = 3
        else:
            maxSubrow = 8

        for subrow in range(0, maxSubrow):
            b |= i[col, row + subrow] << subrow

        bio.write(struct.pack('<B', b))

        col += 1
        if (col % 160) == 0:
            col = 0
            row += 8

    return bio.getvalue()


class Display(Subject):
    def __init__(self):
        self._context = None
        self._bitmap = Image.new(mode='1',
                                 size=(DisplayMetrics.WIDTH_PIXELS,
                                       DisplayMetrics.HEIGHT_PIXELS))

    def getContext(self):
        return PIL.ImageDraw.Draw(self._bitmap)

    def commit(self):
        # convert to LPBM
        # upload to G13
        #
        pass

    def debug(self):
        self._bitmap.show()
