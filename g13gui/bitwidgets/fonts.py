"""
This is a simple library to manage loading X11 PCF bitmap fonts into the PIL.

Unfortunately, PIL is a complete and utter mess of a library that expects to
write it's specific fonts out to *disk*, when it could just convert them in
memory trivially.

Because of the way the FontFile and PcfFontFile and ImageFont classes are
defined, they are hard coded into using file paths rather than using file
pointers, so this does some seriously hacky stuff with internal interfaces to
bludgeon the various classes into behaving correctly.
"""

import io
import gzip
import pathlib
import enum
import PIL
import importlib.resources as pkg_resources
from PIL.ImageFont import ImageFont
from PIL.PcfFontFile import PcfFontFile
from PIL.FontFile import puti16

from . import assets


class Fonts(enum.Enum):
    TINY = '4x6.pcf.gz'
    SMALL = '5x7.pcf.gz'
    MEDIUM = '8x13.pcf.gz'
    LARGE = '9x18.pcf.gz'
    HUGE = '10x20.pcf.gz'


class PcfFontConverter(PcfFontFile):
    """Hacked up PcfFontFile that converts directly to an ImageFont

    This class reimplements the PILfont data format structure in a BytesIO class
    in memory, and then passes both the bitmaps it generates from the PCF file
    on disk and the generated PILfont data to the internal
    ImageFont#_load_pilfont_data interface to construct a proper font for later
    use with an ImageDraw.

    This is all one gigantic horrible hack, and is unlikely to function in
    further revisions of pillow. I hate doing this, but I don't really see any
    other way of managing such a gargantuan mess.
    """

    def _getFontMetricsBuffer(self):
        """Hacky method to generate a PILfont header and then stuff in the
        metrics from a compiled PCF font.

        This is derived from the FontFile#save method.
        """

        bio = io.BytesIO()

        bio.write(b"PILfont\n")
        bio.write((";;;;;;%d;\n" % self.ysize).encode("ascii"))
        bio.write(b"DATA\n")

        for id in range(256):
            m = self.metrics[id]
            if not m:
                puti16(bio, [0] * 10)
            else:
                puti16(bio, m[0] + m[1] + m[2])

        bio.seek(0)
        return bio

    def _getFontBitmap(self):
        return self.bitmap

    def getImageFont(self):
        """Compiles the PCF font into a single image, and then converts it to an
        ImageFont.

        Returns: an ImageFont instance containing the PCF font.
        """

        self.compile()

        fontData = self._getFontMetricsBuffer()
        fontBitmap = self._getFontBitmap()

        imgfont = ImageFont()
        imgfont.file = "Bogus"
        imgfont._load_pilfont_data(fontData, fontBitmap)

        return imgfont


class FontManager(object):
    """Class to load in and initialize the PCF fonts defined in the Fonts enum,
    wrapped all up in a nice interface."""
    _fonts = {}

    def getFont(font):
        """Gets a font, given a font enum.

        If the font isn't loaded yet, this method will load it.

        Returns: an ImageFont
        """
        if len(FontManager._fonts) == 0:
            FontManager._loadFonts()
        return FontManager._fonts[font]

    def _loadPcfFont(filename):
        compressed_data = pkg_resources.read_binary(assets, filename)
        data = gzip.decompress(compressed_data)
        with io.BytesIO(data) as fp:
            pff = PcfFontConverter(fp)
            imageFont = pff.getImageFont()
            return imageFont

    def _loadFonts():
        for (_, enumItem) in Fonts.__members__.items():
            fontpath = enumItem.value
            FontManager._fonts[enumItem] = FontManager._loadPcfFont(fontpath)
