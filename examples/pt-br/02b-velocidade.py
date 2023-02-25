from tupy import *

class Star(Image):
    def __init__(self, velocidade=5):
        self.velocidade = velocidade

    def update(self):
        self.angle = (self.angle + self.velocidade) % 360

s1 = Star()
s2 = Star(7)

run(globals())