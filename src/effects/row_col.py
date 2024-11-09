"""
row_col.py
"""

from effects import RAINBOW, EffectBase


class RowCol(EffectBase):
    """
    RowCol effect class to display a row or column of color on the matrix.

    Attributes:
        help_purpose (str): Description of the effect's purpose.
        help_json (str): JSON representation of the effect.
        index (int): Current index in the RAINBOW color list.
        is_row (bool): Flag to determine if the effect is applied to rows or columns.
        current_row_col (int): Current row or column index.
    """

    help_purpose = "Display a row or column of color on the matrix."

    def __init__(self, matrix, params):
        super().__init__(matrix, params)
        self._index = 0
        self._is_row = True
        self._current_row_col = 0

    def _incr_index(self):
        """
        Increment the index and reset if it exceeds the length of RAINBOW.

        Returns:
            bool: True if the index was reset, False otherwise.
        """
        self._index = self._index + 1
        if self._index >= len(RAINBOW):
            self._index = 0
            return True
        return False

    def _incr_row_col(self):
        """
        Increment the current row or column index and switch between rows and columns.

        Returns:
            bool: True if the row/column index was reset and switched, False otherwise.
        """
        self._current_row_col = self._current_row_col + 1
        max_row_col = self._matrix.n_rows if self._is_row else self._matrix.n_cols
        if self._current_row_col >= max_row_col:
            self._current_row_col = 0
            self._is_row = not self._is_row
            return True
        return False

    def advance(self):
        """
        Advance to the next row or column and update the color index if needed.
        """
        if self._incr_row_col():
            self._incr_index()

    def render(self):
        """
        Render the current row or column with the current color.
        """
        m = self._matrix
        m.clear()
        if self._is_row:
            m.line(
                self._current_row_col,
                0,
                self._current_row_col,
                m.n_cols - 1,
                color=RAINBOW[self._index],
            )
        else:
            m.line(
                m.n_rows - 1,
                self._current_row_col,
                0,
                self._current_row_col,
                color=RAINBOW[self._index],
            )
        m.write()


register = (RowCol,)
