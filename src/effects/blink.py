from . import EffectBase


class Blink(EffectBase):
    
    help_purpose = "blinking lights, choose between patches and rows."
    
    def __init__(self, matrix, params):
        
        super().__init__(matrix, params)
        self.matrix = matrix
        self.timestep = 0
        self._wait = params.get("wait", 500)
        self.style = params.get("style", "patch")

        self.color_1 = (50, 10, 25)
        self.color_2 = (13, 50, 8)
        self.color_3 = (3, 13, 50)
        self.color_4 = (128, 20, 18)
        
        if self.style == "row":
            self.indices = (0, 2, 3, 5, 6, 8, 9, 11)
        else:
            self.indices = (0, 2, 4, 6, 8, 10)

    def advance(self):
        self.timestep += 1
        if self.timestep % 5 == 0:
            self.color_1, self.color_2, self.color_3, self.color_4 = self.color_3, self.color_4, self.color_1, self.color_2


    def render(self):
        for i in range(self.matrix.size()):
            if self.timestep % 2 == 0:
                if i in self.indices:
                    self.matrix.set_index(i, self.color_1)
                else:
                    self.matrix.set_index(i, self.color_2)  
            else:
                if i in self.indices:
                    self.matrix.set_index(i, self.color_2)
                else:
                    self.matrix.set_index(i, self.color_1)


        self.matrix.write()

register = (Blink,)
