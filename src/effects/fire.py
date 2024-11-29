"""
fire.py - Display a fire on the matrix
"""

from . import EffectBase
from random import randint


# Create an array to store the brightness values for each LED


# Helper function to calculate heat color based on temperature
def HeatColor(temperature):
  if (temperature < 85):
    color = (temperature * 3, 0, 0)
  else:
    color = (255, (temperature - 85) * 3, 0)
  
  return color


# Helper function to subtract two 8-bit values with saturation
def qsub8(a, b):
    if (b > a): 
        return 0
    return a - b

# Helper function to add two 8-bit values with saturation
def qadd8(a, b):
    sum = a + b
    if (sum < a): 
        return 255

    return sum



class Fire(EffectBase):
    """
    Fire effect class to display a rainbow on the matrix.

    Attributes:
        help_purpose (str): Description of the effect's purpose.
        help_json (str): JSON representation of the effect.
        rainbow (list): List of colors representing the rainbow.
        start_ms (int): Start time in milliseconds.
    """

    help_purpose = "Display a fire on the matrix."

    def __init__(self, matrix, params):
        """
        Initialize the Fire effect.

        Args:
            matrix: The matrix object to apply the effect on.
            params: Additional parameters for the effect.
        """
        super().__init__(matrix, params)
        m = self._matrix
        msize = m.size()
        self.heat = [0 for i in range(msize)]

    def advance(self):
        """
        Advance the rainbow effect by rotating the colors.
        """
        # Calculate the heat for each LED
        m = self._matrix
        msize = m.size()
        for i in range(msize):
            # Randomly increase the heat for each LED
            self.heat[i] = qsub8(self.heat[i], randint(0, 32))


        # Apply cooling effect to each LED
        for i in range(msize):
            if (randint(0, 10) < 3):
                self.heat[i] = qadd8(self.heat[i], randint(0, 96))

    def render(self):
        """
        Render the fire effect on the matrix.
        """  

        m = self._matrix
        for i in range(m.size()):
            m.set_index(i, HeatColor(self.heat[i]))
        m.write()


register = (Fire,)