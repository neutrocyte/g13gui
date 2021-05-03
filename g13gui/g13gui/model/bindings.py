#!/usr/bin/python3

import gi
from evdev import ecodes as e

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, GObject, Gdk

from g13gui.g13.common import G13Keys

"""
Defines a whole bunch of constants relating to mapping G13D key names to GDK
key names, as well as the symbols that g13d natively supports.
"""

DEFAULT_KEY_BINDINGS = {
    G13Keys.G1.name: [e.KEY_GRAVE],
    G13Keys.G2.name: [e.KEY_1],
    G13Keys.G3.name: [e.KEY_2],
    G13Keys.G4.name: [e.KEY_3],
    G13Keys.G5.name: [e.KEY_4],
    G13Keys.G6.name: [e.KEY_5],
    G13Keys.G7.name: [e.KEY_6],
    G13Keys.G8.name: [e.KEY_TAB],
    G13Keys.G9.name: [e.KEY_Q],
    G13Keys.G10.name: [e.KEY_W],
    G13Keys.G11.name: [e.KEY_E],
    G13Keys.G12.name: [e.KEY_R],
    G13Keys.G13.name: [e.KEY_T],
    G13Keys.G14.name: [e.KEY_Y],
    G13Keys.G15.name: [e.KEY_A],
    G13Keys.G16.name: [e.KEY_S],
    G13Keys.G17.name: [e.KEY_D],
    G13Keys.G18.name: [e.KEY_F],
    G13Keys.G19.name: [e.KEY_G],
    G13Keys.G20.name: [e.KEY_X],
    G13Keys.G21.name: [e.KEY_C],
    G13Keys.G22.name: [e.KEY_V],
    G13Keys.THUMB_LEFT.name: [e.KEY_B],
    G13Keys.THUMB_DOWN.name: [e.KEY_N],
}


class StickRegion():
    UP = 'STICK_UP'
    DOWN = 'STICK_DOWN'
    LEFT = 'STICK_LEFT'
    RIGHT = 'STICK_RIGHT'


ALL_STICK_REGIONS = frozenset({
    StickRegion.UP, StickRegion.DOWN,
    StickRegion.LEFT, StickRegion.RIGHT
})


DEFAULT_STICK_REGIONS = {
    StickRegion.UP:    [0.0, 0.0, 1.0, 0.2],
    StickRegion.DOWN:  [0.0, 0.8, 1.0, 1.0],
    StickRegion.LEFT:  [0.0, 0.0, 0.2, 1.0],
    StickRegion.RIGHT: [0.8, 0.0, 1.0, 1.0]
}

DEFAULT_STICK_REGION_BINDINGS = {
    StickRegion.UP:    [e.KEY_W],
    StickRegion.DOWN:  [e.KEY_S],
    StickRegion.LEFT:  [e.KEY_A],
    StickRegion.RIGHT: [e.KEY_D]
}


class StickMode(object):
    ABSOLUTE = 'ABSOLUTE'
    RELATIVE = 'RELATIVE'
    KEYS = 'KEYS'


ALL_STICK_MODES = frozenset({
    StickMode.ABSOLUTE, StickMode.RELATIVE, StickMode.KEYS
})


DEFAULT_LCD_COLOR = (1.0, 0.0, 0.0)


def KeycodeIsModifier(code):
    return code in (
        e.KEY_LEFTSHIFT, e.KEY_RIGHTSHIFT,
        e.KEY_LEFTCTRL, e.KEY_RIGHTCTRL,
        e.KEY_LEFTALT, e.KEY_RIGHTALT)


def BindsToKeynames(binds):
    keybinds = []
    for bind in binds:
        name = e.KEY[bind][4:].capitalize()
        keybinds.append(name)

    return keybinds
