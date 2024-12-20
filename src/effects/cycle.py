"""
cycle.py - Cycle effect class to cycle through the matrix.
Author: Karijn Wessing, Sensemakers Amsterdam
Maintainer: Sensemakers Amsterdam  https://sensemakersams.org
"""
from . import EffectBase, text2color


class Cycle(EffectBase):
    """
    Cycle effect class to cycle through the matrix.

    Attributes:
        help_purpose (str): Description of the effect's purpose.
        help_json (str): JSON representation of the effect.
        index (int): Current index in the matrix.
        color (tuple): Color to be displayed.
    """

    help_purpose = "Cycle through the matrix."
    help_json = '{ "effect": "cycle", "color": "(200,30,4)" }'

    def __init__(self, matrix, params):
        """
        Initialize the Cycle effect.

        Args:
            matrix: The matrix object to apply the effect on.
            params: Additional parameters for the effect.
        """
        super().__init__(matrix, params)
        self._index = 0
        self._color = text2color(params)

    def advance(self):
        """
        Advance the cycle effect by incrementing the index.
        """
        self._index += 1

    def render(self):
        """
        Render the cycle effect on the matrix.
        """
        m = self._matrix
        m.clear(show=False)
        m.set_index(self._index % m.size(), self._color, show=True)


register = (Cycle,)
