from . import EffectBase


class Cycle(EffectBase):
    def __init__(self, matrix, msg):
        super().__init__(matrix, msg)
        self.index = 0
        self.color = self.msg.get("color", (255, 0, 0))
        print(self.color)

    def advance(self):
        self.index += 1

    def render(self):
        self.matrix.clear(show=False)
        self.matrix.set_index(self.index % self.matrix.size(), self.color, show=True)
