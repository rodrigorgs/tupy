from tupy import *

class Star(Image):
    def update(self):
        self.angle = (self.angle + 5) % 360

_label1 = Label('Crie um atributo para definir a velocidade de rotação.', 5, 5)
_label2 = Label('Para isso, adicione o método __init__(self).', 5, 30)
s1 = Star()
s2 = Star()

run(globals())