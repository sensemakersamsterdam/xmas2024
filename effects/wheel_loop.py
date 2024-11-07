from effects import EffectBase, wheel

class WheelLoop(EffectBase):
    """
    WheelLoop effect class to cycle through the matrix with a wheel effect.

    Attributes:
        help_purpose (str): Description of the effect's purpose.
        help_json (str): JSON representation of the effect.
        index (int): Current index for the wheel effect.
    """
    help_purpose = "Cycle through the matrix with a wheel effect."
    help_json = '{ "effect": "wheel_loop" }'

    def __init__(self, matrix, params):
        """
        Initialize the WheelLoop effect.

        Args:
            matrix: The matrix object to apply the effect on.
            params: Additional parameters for the effect.
        """
        super().__init__(matrix, params)
        self._index = 0

    def advance(self):
        """
        Advance the wheel effect by incrementing the index.
        """
        self._index += 1

    def render(self):
        """
        Render the wheel effect on the matrix.
        """
        m = self._matrix
        msize = m.size()
        for i in range(msize):
            rc_index = (i * 256 // msize) + self._index
            m.set_index(i, wheel(rc_index & 255))
        m.write()

register = (WheelLoop,)
