"""
effect_base.py
"""

from time import ticks_ms


class Effects(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Effects, cls).__new__(cls)
            cls.instance.effects = {}
        return cls.instance

    def add(cls, k: str, c):
        cls.instance.effects[k.lower()] = c

    def all(cls):
        return cls.instance.effects.keys()

    def get(cls, k, d):
        return cls.instance.effects.get(k.lower(), d)

    def help(cls):
        ret = "Effects: " + ", ".join(cls.instance.effects)
        return ret


class EffectBase:
    def __init__(self, matrix, msg=None):
        self.matrix = matrix
        self.msg = msg
        self.start_ms = ticks_ms()
        self.start()
        self.wait = 100

    def help_text(self):
        return "No more help"

    def start(self):
        self.matrix.clear()

    def render(self):
        raise NotImplementedError("set")

    def advance(self):
        raise NotImplementedError("advance") 

    def loop(self):
        if ticks_ms() > self.start_ms + self.wait:
            self.render()
            self.advance()
            self.start_ms = ticks_ms()

    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

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
