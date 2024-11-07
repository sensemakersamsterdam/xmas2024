"""
rainbow.py - Display a rainbow on the matrix
"""

from . import EffectBase, RAINBOW

class Rainbow(EffectBase):
    """
    Rainbow effect class to display a rainbow on the matrix.

    Attributes:
        help_purpose (str): Description of the effect's purpose.
        help_json (str): JSON representation of the effect.
        rainbow (list): List of colors representing the rainbow.
        start_ms (int): Start time in milliseconds.
    """
    help_purpose = "Display a rainbow on the matrix."
    help_json = '{ "effect": "rainbow" }'

    def __init__(self, matrix, params):
        """
        Initialize the Rainbow effect.

        Args:
            matrix: The matrix object to apply the effect on.
            params: Additional parameters for the effect.
        """
        super().__init__(matrix, params)
        self._rainbow = list(RAINBOW)

    def advance(self):
        """
        Advance the rainbow effect by rotating the colors.
        """
        self._rainbow = self._rainbow[-1:] + self._rainbow[:-1]

    def render(self):
        """
        Render the rainbow effect on the matrix.
        """
        m = self._matrix
        for i in range(m.size()):
            m.set_index(i, self._rainbow[i])
        m.write()

register = (Rainbow,)
