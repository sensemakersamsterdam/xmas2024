"""
rainbow.py - Display a rainbow on the matrix
"""

from time import ticks_ms
from . import EffectBase


class Rainbow(EffectBase):
    rainbow = [
        (126, 1, 0),
        (114, 13, 0),
        (102, 25, 0),
        (90, 37, 0),
        (78, 49, 0),
        (66, 61, 0),
        (54, 73, 0),
        (42, 85, 0),
        (30, 97, 0),
        (18, 109, 0),
        (6, 121, 0),
        (0, 122, 5),
        (0, 110, 17),
        (0, 98, 29),
        (0, 86, 41),
        (0, 74, 53),
        (0, 62, 65),
        (0, 50, 77),
        (0, 38, 89),
        (0, 26, 101),
        (0, 14, 113),
        (0, 2, 125),
        (9, 0, 118),
        (21, 0, 106),
        (33, 0, 94),
        (45, 0, 82),
        (57, 0, 70),
        (69, 0, 58),
        (81, 0, 46),
        (93, 0, 34),
        (105, 0, 22),
        (117, 0, 10),
    ]

    def advance(self):
        self.rainbow = self.rainbow[-1:] + self.rainbow[:-1]

    def render(self):
        for i in range(self.matrix.size()):
            self.matrix.set_index(i, self.rainbow[i])
        self.matrix.write()

    def loop(self):
        if ticks_ms() > self.start_ms + 100:
            self.advance()
            self.render()
            self.start_ms = ticks_ms()
