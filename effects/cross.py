"""
red_cross.py - Display a red cross on the matrix
"""

from . import EffectBase


class Cross(EffectBase):
    def __init__(self, matrix, msg):
        super().__init__(matrix, msg)
        self.index = 0
        self.is_on = True
        self.wait = 500

    def render(self):
        if self.is_on:
            self.matrix.clear()
        else:
            m = self.matrix
            m.line(
                0, 0, self.matrix.n_rows - 1, self.matrix.n_cols - 1, color=(255, 0, 0)
            )
            m.line(
                self.matrix.n_rows - 1, 0, 0, self.matrix.n_cols - 1, color=(255, 0, 0)
            )
            m.write()
        self.is_on = not self.is_on
