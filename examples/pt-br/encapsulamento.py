from tupy import *

class Star(BaseImage):
    def __init__(self):
        self._file = 'star2.png'
        self._ligado = False
        self._x = 20
        self._y = 100
        self._velocidade = 0

    def desliga(self):
        self._file = 'star2.png'
        self._ligado = False
    
    def liga(self):
        self._file = 'star.png'
        self._ligado = True

    @property
    def estado(self):
        if self._ligado:
            return 'ligado'
        else:
            return 'desligado'
    
    def update(self):
        self._x = (self._x + self._velocidade) % 640
    
    def acelera(self):
        if self._ligado:
            self._velocidade += 1
            if self._velocidade > 10:
                self._velocidade = 10
    
    def freia(self):
        self._velocidade -= 1
        if self._velocidade < 0:
            self._velocidade = 0
    
    @property
    def velocidade(self):
        return self._velocidade

_label1 = Label('Experimente chamar os métodos da estrela', 5, 5)
_label2 = Label('(por exemplo, liga e desliga)', 5, 30)
s1 = Star()
run(globals())