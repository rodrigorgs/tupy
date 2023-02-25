from tupy import *

class Star(Image):
    def update(self):
        self.angle = (self.angle + 5) % 360

s1 = Star()
s2 = Star()

run(globals())