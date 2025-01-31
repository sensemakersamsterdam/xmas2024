"""
xmas_tree.py - Display a red cross on the matrix
"""

from . import EffectBase, random_color, fader, wheel
from random import randint


class XmasTree(EffectBase):
    """
    Xmas Tree effect class to display a Tree, its outline and ornaments on the matrix.

    Attributes:
        help_purpose (str): Description of the effect's purpose.
        help_json (str): JSON representation of the effect.
        is_on (bool): Flag to determine if the cross is currently displayed.
        wait (int): Wait time in milliseconds between toggles.
        color (tuple): Color of the cross.
    """

    help_purpose = "Display the Tree, it's outline, and ornament on the matrix."
    help_json = '{ "effect": "xmastree", "color": "(200,0,0)", "wait": 500 }'

    def __init__(self, matrix, params):
        """
        Initialize the Cross effect.

        Args:
            matrix: The matrix object to apply the effect on.
            params: Additional parameters for the effect.
        """
        super().__init__(matrix, params)
        self._matrix.clear()
        self._is_on = True
        self._wait = params.get("wait", 500)
        self._color = eval(params.get("color", "(0, 255, 0)"))
        self._treecolors = [(0,128,0),
                            (0,100,0),
                            (17,139,17),
                            (23,139,43),
                            (0,107,60)]
        self.tree_index = 0
        self.tree_max = 10
        self.tree_start = random_color(self._treecolors)
        self.tree_end   = random_color(self._treecolors)
        self.outline_index = 0
        self.outline_max = 40
        self.outline_start = (0, 255, 0)
        self.outline_end = (127, 0, 0)
        
        self.ornament_index = [0, 0, 0, 0]
        
        self.ornament_max = 10
        self.ornament_start = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        self.ornament_running = [False, False, False, False]
#         for col in range(4):
#             self.ornament_start[col] = (0, 0, 0)
#             self.ornament_running[col] = False
        self.ornament_end    = (0, 0, 0)
        
    def render(self):
        """
        Render the cross effect on the matrix.
        """
        #if self._is_on:
        #    self._matrix.clear()
        #else:
        m = self._matrix
        
        # draw tree
        m.line(2, 0, 2, m.n_cols - 1, color=fader(self.tree_index, self.tree_max, self.tree_start, self.tree_end))

        # draw outline
        m.line(1, 0, 1, m.n_cols - 1, color=fader(self.outline_index, self.outline_max, self.outline_start, self.outline_end))
        
        # draw ornaments
        for col in range(4):
            m.set_pix(0, col, color=fader(self.ornament_index[col], self.ornament_max, self.ornament_start[col], self.ornament_end))

        m.write()

    def advance(self):
        """
        Advance the cross effect by toggling the display state.
        """
        self._is_on = not self._is_on
        
        self.tree_index = self.tree_index + 1
        if self.tree_index == self.tree_max:
            self.tree_index = 0
            self.tree_start = self.tree_end
            self.tree_end   = random_color(self._treecolors)

        self.outline_index = self.outline_index + 1
        if self.outline_index == self.outline_max:
            self.outline_index = 0
            (self.outline_start, self.outline_end) = (self.outline_end, self.outline_start)

        for col in range(4):
            if self.ornament_running[col]:
                self.ornament_index[col] = self.ornament_index[col] + 1 
                if self.ornament_index[col] == self.ornament_max:
                    self.ornament_start[col] = self.ornament_end
                    self.ornament_running[col] = False
                
        col = randint(0, 30)
        if col >= 0 and col < 4:
            self.ornament_running[col] = True
            self.ornament_start[col] = wheel(randint(0, 255))
            self.ornament_index[col] = 0
            
            
register = (XmasTree,)


