
from effects import EffectBase


class WheelLoop(EffectBase):
    def __init__(self, matrix, msg):
        super().__init__(matrix, msg)
        self.index = 0

    def advance(self):
        self.index = self.index + 1

    def render(self):
        for i in range(self.matrix.size()):
            rc_index = (i * 256 // self.matrix.size()) + self.index
            self.matrix.set_index(i, self.wheel(rc_index & 255))
        self.matrix.write()