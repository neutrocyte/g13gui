#!/usr/bin/python3

import enum


G13D_TO_GDK_KEYBINDS = {
    '0': '0',
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    'A': 'A',
    'B': 'B',
    'C': 'C',
    'D': 'D',
    'E': 'E',
    'F': 'F',
    'G': 'G',
    'H': 'H',
    'I': 'I',
    'J': 'J',
    'K': 'K',
    'L': 'L',
    'M': 'M',
    'N': 'N',
    'O': 'O',
    'P': 'P',
    'Q': 'Q',
    'R': 'R',
    'S': 'S',
    'T': 'T',
    'U': 'U',
    'V': 'V',
    'W': 'W',
    'X': 'X',
    'Y': 'Y',
    'Z': 'Z',

    'LEFT': 'Left',
    'RIGHT': 'Right',
    'UP': 'Up',
    'DOWN': 'Down',

    'APOSTROPHE': 'apostrophe',
    'BACKSLASH': 'backslash',
    'BACKSPACE': 'backspace',
    'CAPSLOCK': 'capslock',
    'COMMA': 'comma',
    'DOT': 'period',
    'ENTER': 'enter',
    'EQUAL': 'equals',
    'ESC': 'Escape',
    'F1': 'F1',
    'F2': 'F2',
    'F3': 'F3',
    'F4': 'F4',
    'F5': 'F5',
    'F6': 'F6',
    'F7': 'F7',
    'F8': 'F8',
    'F9': 'F9',
    'F10': 'F10',
    'F11': 'F11',
    'F12': 'F12',
    'GRAVE': 'grave',

    'INSERT': 'insert',
    'HOME': 'home',
    'PAGEUP': 'pageup',
    'DELETE': 'delete',
    'END': 'end',
    'PAGEDOWN': 'pagedown',

    'NUMLOCK': 'numlock',
    'KPASTERISK': 'kpasterisk',
    'KPMINUS': '0',
    'KP7': '0',
    'KP8': '0',
    'KP9': '0',
    'KPPLUS': '0',
    'KP4': '0',
    'KP5': '0',
    'KP6': '0',
    'KP1': '0',
    'KP2': '0',
    'KP3': '0',
    'KP0': '0',
    'KPDOT': '0',

    'LEFTBRACE': 'braceleft',
    'RIGHTBRACE': 'braceright',
    'MINUS': 'minus',
    'SEMICOLON': 'semicolon',
    'SLASH': 'slash',
    'SPACE': 'space',
    'TAB': 'Tab',

    'LEFTALT': 'Alt_L',
    'LEFTCTRL': 'Control_L',
    'LEFTSHIFT': 'Shift_L',
    'RIGHTALT': 'Alt_R',
    'RIGHTCTRL': 'Control_R',
    'RIGHTSHIFT': 'Shift_R',
    'SCROLLLOCK': 'ScrollLock',
}

GDK_TO_G13D_KEYBINDS = {}
for g13d_key, gdk_key in G13D_TO_GDK_KEYBINDS.items():
    GDK_TO_G13D_KEYBINDS[gdk_key] = g13d_key

GDK_TO_G13D_KEYBINDS['asciitilde'] = 'GRAVE'
GDK_TO_G13D_KEYBINDS['braceleft'] = 'LEFTBRACE'
GDK_TO_G13D_KEYBINDS['braceright'] = 'RIGHTBRACE'
GDK_TO_G13D_KEYBINDS['bracketleft'] = 'LEFTBRACE'
GDK_TO_G13D_KEYBINDS['bracketright'] = 'RIGHTBRACE'
GDK_TO_G13D_KEYBINDS['quotedbl'] = 'APOSTROPHE'
GDK_TO_G13D_KEYBINDS['less'] = 'COMMA'
GDK_TO_G13D_KEYBINDS['greater'] = 'DOT'
GDK_TO_G13D_KEYBINDS['bar'] = 'BACKSLASH'
GDK_TO_G13D_KEYBINDS['question'] = 'SLASH'
GDK_TO_G13D_KEYBINDS['colon'] = 'SEMICOLON'
GDK_TO_G13D_KEYBINDS['plus'] = 'EQUALS'
GDK_TO_G13D_KEYBINDS['exclam'] = '1'
GDK_TO_G13D_KEYBINDS['at'] = '2'
GDK_TO_G13D_KEYBINDS['numbersign'] = '3'
GDK_TO_G13D_KEYBINDS['dollar'] = '4'
GDK_TO_G13D_KEYBINDS['percent'] = '5'
GDK_TO_G13D_KEYBINDS['asciicircum'] = '6'
GDK_TO_G13D_KEYBINDS['ampersand'] = '7'
GDK_TO_G13D_KEYBINDS['asterisk'] = '8'
GDK_TO_G13D_KEYBINDS['parenleft'] = '9'
GDK_TO_G13D_KEYBINDS['parenright'] = '0'
GDK_TO_G13D_KEYBINDS['ISO_Left_Tab'] = 'TAB'

G13_KEYS = [
    'BD', 'L1', 'L2', 'L3', 'L4', 'LIGHT',
    'M1', 'M2', 'M3', 'MR',
    'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7',
    'G8', 'G9', 'G10', 'G11', 'G12', 'G13', 'G14',
    'G15', 'G16', 'G17', 'G18', 'G19',
    'G20', 'G21', 'G22',
    'LEFT', 'DOWN', 'TOP',
]

DEFAULT_STICK_REGIONS = {
    'STICK_UP':    [0.0, 0.0, 1.0, 0.2],
    'STICK_DOWN':  [0.0, 0.8, 1.0, 1.0],
    'STICK_LEFT':  [0.0, 0.0, 0.2, 1.0],
    'STICK_RIGHT': [0.8, 0.0, 1.0, 1.0]
}

DEFAULT_KEY_BINDINGS = {
    'G1': ['ESC'],
    'G2': ['1'],
    'G3': ['2'],
    'G4': ['3'],
    'G5': ['4'],
    'G6': ['5'],
    'G7': ['Y'],
    'G8': ['Q'],
    'G9': ['Z'],
    'G10': ['V'],
    'G11': ['SPACE'],
    'G12': ['E'],
    'G13': ['R'],
    'G14': ['U'],
    'G15': ['LEFTSHIFT'],
    'G16': ['F'],
    'G17': ['X'],
    'G18': ['C'],
    'G19': ['H'],
    'G20': ['LEFTCTRL'],
    'G21': ['B'],
    'G22': ['T'],
    'LEFT': ['TAB'],
    'DOWN': ['M'],
}


class StickRegion(enum.Enum):
    UP = 'STICK_UP'
    DOWN = 'STICK_DOWN'
    LEFT = 'STICK_LEFT'
    RIGHT = 'STICK_RIGHT'


ALL_STICK_REGIONS = frozenset({
    StickRegion.UP,
    StickRegion.DOWN,
    StickRegion.LEFT,
    StickRegion.RIGHT
})


DEFAULT_STICK_REGION_BINDINGS = {
    StickRegion.UP: ['W'],
    StickRegion.DOWN: ['S'],
    StickRegion.LEFT: ['A'],
    StickRegion.RIGHT: ['D']
}


class StickMode(enum.Enum):
    ABSOLUTE = 'ABSOLUTE'
    RELATIVE = 'RELATIVE'
    KEYS = 'KEYS'


ALL_STICK_MODES = frozenset({
    StickMode.ABSOLUTE,
    StickMode.RELATIVE,
    StickMode.KEYS
})

def G13DKeyIsModifier(key):
    key = key.upper()
    return (key == 'LEFTSHIFT' or key == 'RIGHTSHIFT' or
            key == 'LEFTALT' or key == 'RIGHTALT' or
            key == 'LEFTCTRL' or key == 'RIGHTCTRL')
