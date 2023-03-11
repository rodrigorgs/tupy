from tupy import *

class Star(Image):
    pass

_label1 = Label('Altere o ângulo de uma estrela através do editor.', 5, 5)
_label2 = Label('A seguir, altere o código para fazer as estrelas girarem automaticamente.', 5, 30)
_label3 = Label('Para isso, adicione o método update(self) à classe Star.', 5, 55)
s1 = Star()
s2 = Star()

run(globals())