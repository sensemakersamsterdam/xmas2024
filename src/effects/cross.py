"""
cross.py - Display a red cross on the matrix
Author: Karijn Wessing, Sensemakers Amsterdam
Maintainer: Sensemakers Amsterdam  https://sensemakersams.org
"""

from . import EffectBase, text2color
import senselogging as logging


class Cross(EffectBase):
    """
    Cross effect class to display a red cross on the matrix.

    Attributes:
        help_purpose (str): Description of the effect's purpose.
        help_json (str): JSON representation of the effect.
        is_on (bool): Flag to determine if the cross is currently displayed.
        wait (int): Wait time in milliseconds between toggles.
        color (tuple): Color of the cross.
    """

    help_purpose = "Display a red cross on the matrix."
    help_json = '{ "effect": "cross", "color": "(200,0,0)", "wait": 500 }'

    def __init__(self, matrix, params):
        """
        Initialize the Cross effect.

        Args:
            matrix: The matrix object to apply the effect on.
            params: Additional parameters for the effect.
        """
        super().__init__(matrix, params)
        self._is_on = True
        self._wait = params.get("wait", 500)
        self._color = text2color(params)

    def render(self):
        """
        Render the cross effect on the matrix.
        """
        if self._is_on:
            self._matrix.clear()
        else:
            m = self._matrix
            m.line(0, 0, m.n_rows - 1, m.n_cols - 1, color=self._color)
            m.line(m.n_rows - 1, 0, 0, m.n_cols - 1, color=self._color)
            m.write()

    def advance(self):
        """
        Advance the cross effect by toggling the display state.
        """
        self._is_on = not self._is_on


register = (Cross,)
