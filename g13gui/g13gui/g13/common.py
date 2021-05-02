import enum


class G13Keys(enum.Enum):
    G1 = {'byte': 3, 'bit': 0}
    G2 = {'byte': 3, 'bit': 1}
    G3 = {'byte': 3, 'bit': 2}
    G4 = {'byte': 3, 'bit': 3}
    G5 = {'byte': 3, 'bit': 4}
    G6 = {'byte': 3, 'bit': 5}
    G7 = {'byte': 3, 'bit': 6}
    G8 = {'byte': 3, 'bit': 7}
    G9 = {'byte': 4, 'bit': 0}
    G10 = {'byte': 4, 'bit': 1}
    G11 = {'byte': 4, 'bit': 2}
    G12 = {'byte': 4, 'bit': 3}
    G13 = {'byte': 4, 'bit': 4}
    G14 = {'byte': 4, 'bit': 5}
    G15 = {'byte': 4, 'bit': 6}
    G16 = {'byte': 4, 'bit': 7}
    G17 = {'byte': 5, 'bit': 0}
    G18 = {'byte': 5, 'bit': 1}
    G19 = {'byte': 5, 'bit': 2}
    G20 = {'byte': 5, 'bit': 3}
    G21 = {'byte': 5, 'bit': 4}
    G22 = {'byte': 5, 'bit': 5}
    BD = {'byte': 6, 'bit': 0}
    L1 = {'byte': 6, 'bit': 1}
    L2 = {'byte': 6, 'bit': 2}
    L3 = {'byte': 6, 'bit': 3}
    L4 = {'byte': 6, 'bit': 4}
    M1 = {'byte': 6, 'bit': 5}
    M2 = {'byte': 6, 'bit': 6}
    M3 = {'byte': 6, 'bit': 7}
    MR = {'byte': 7, 'bit': 0}
    THUMB_LEFT = {'byte': 7, 'bit': 1}
    THUMB_DOWN = {'byte': 7, 'bit': 2}
    THUMB_STICK = {'byte': 7, 'bit': 3}

    def testReport(self, report):
        byte = self.value['byte']
        bit = 1 << self.value['bit']
        return (report[byte] & bit) == bit


G13NormalKeys = frozenset({
    G13Keys.G1, G13Keys.G2, G13Keys.G3, G13Keys.G4, G13Keys.G5, G13Keys.G6,
    G13Keys.G7, G13Keys.G8, G13Keys.G9, G13Keys.G10, G13Keys.G11, G13Keys.G12,
    G13Keys.G13, G13Keys.G14, G13Keys.G15, G13Keys.G16, G13Keys.G17,
    G13Keys.G18, G13Keys.G19, G13Keys.G20, G13Keys.G21, G13Keys.G22,
    G13Keys.THUMB_LEFT, G13Keys.THUMB_DOWN, G13Keys.THUMB_STICK
})

G13SpecialKeys = frozenset({
    G13Keys.BD, G13Keys.L1, G13Keys.L2, G13Keys.L3, G13Keys.L4,
    G13Keys.M1, G13Keys.M2, G13Keys.M3, G13Keys.MR,
})
