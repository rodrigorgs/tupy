from tupy import *

class Star(Image):
    def __init__(self):
        self.file = 'star.png'
        self.x = 0
        self._ligado = True
        self.velocidade = 5

    def desliga(self):
        self.file = 'star2.png'
        self._ligado = False
    
    def liga(self):
        self.file = 'star.png'
        self._ligado = True

    def estado(self):
        if self._ligado:
            return 'ligado'
        else:
            return 'desligado'
    
    def update(self):
        if self._ligado:
            self.x = (self.x + self.velocidade) % 640

_label1 = Label('Experimente chamar os métodos das estrelas', 5, 5)
_label2 = Label('(por exemplo, liga e desliga)', 5, 30)
s1 = Star()
s2 = Star()

s1.y = 150
s2.y = 250

run(globals())