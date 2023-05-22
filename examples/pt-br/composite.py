from tupy import *

remove_public_members()

class Star(Image):
    def update(self):
        self._angle += 3

class Carta(Composite):
    def __init__(self, valor, cor, x, y) -> None:
        self.carta = Image()
        self.carta._file = 'carta.png'
        self.carta._x = 0
        self.carta._y = 0
        self.label = Label(valor, -50, -115)
        self.label._color = cor
        self._add(self.carta)
        self._add(self.label)
        star = Star()
        star._x = 0
        star._y = 0
        self._add(star)
        self._x = x
        self._y = y
    
c = Carta('A', 'red', 200, 200)
d = Carta('2', 'black', 400, 200)

run(globals())