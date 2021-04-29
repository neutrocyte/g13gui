from g13gui.bitwidgets import Fonts
from g13gui.bitwidgets import FontManager
from g13gui.bitwidgets import Display


d = Display()
ctx = d.getContext()
ctx.text((0, 0), "Hello world!",
         font=FontManager.getFont(Fonts.TINY),
         fill=(1))
ctx.text((0, 6), "Hello world!",
         font=FontManager.getFont(Fonts.MEDIUM),
         fill=(1))
ctx.text((0, 11), "Hello world!",
         font=FontManager.getFont(Fonts.LARGE),
         fill=(1))
ctx.text((0, 19), "Hello world!",
         font=FontManager.getFont(Fonts.HUGE),
         fill=(1))
d.debug()
