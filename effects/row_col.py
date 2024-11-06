"""
row_col.py
"""



from . import EffectBase


class RowCol(EffectBase):
    """
    RowColl effect
    Params:
        None
    """

    def __init__(self, matrix, msg):
        super().__init__(matrix, msg)

        self.index = 0
        self.is_row = True
        self.current_row_col = 0

    def help_text(self):
        return "Help on RowCol"

    def incr_index(self):
        self.index = self.index + 1
        if self.index >= len(self.rainbow):
            self.index = 0
            return True
        return False

    def incr_row_col(self):
        self.current_row_col = self.current_row_col + 1
        max_row_col = self.matrix.n_rows if self.is_row else self.matrix.n_cols
        if self.current_row_col >= max_row_col:
            self.current_row_col = 0
            self.is_row = False if self.is_row else True
            return True
        return False

    def advance(self):
        if self.incr_row_col():
            self.incr_index()

    def render(self):
        self.matrix.clear()
        if self.is_row:
            self.matrix.line(
                self.current_row_col,
                0,
                self.current_row_col,
                self.matrix.n_cols - 1,
                color=EffectBase.rainbow[self.index],
            )
        else:
            self.matrix.line(
                self.matrix.n_rows - 1,
                self.current_row_col,
                0,
                self.current_row_col,
                color=EffectBase.rainbow[self.index],
            )
        self.matrix.write()