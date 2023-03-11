from tupy import *

class Drone(Image):
    def __init__(self):
        self.x = 50
        self.y = 50

    def move_para_cima(self):
        if self.y > 50:
            self.y -= 100
            self._atualiza()

    def move_para_baixo(self):
        if self.y < 250:
            self.y += 100
            self._atualiza()
    
    def move_para_esquerda(self):
        if self.x > 50:
            self.x -= 100
            self._atualiza()
    
    def move_para_direita(self):
        if self.x < 250:
            self.x += 100
            self._atualiza()

    def _atualiza(self):
        itens = [v for k, v in globals().items() if isinstance(v, Estrela)]
        for item in itens:
            if self.collides_with(item):
                item.acende()

class Estrela(Image):
    def __init__(self, x, y):
        self.file = 'star2.png'
        self.x = x
        self.y = y
        self._acesa = False

    def update(self):
        self.angle = (self.angle + 5) % 360

    @property
    def acesa(self):
        return self._acesa
    @acesa.setter
    def acesa(self, valor):
        if valor:
            self.acende()
        else:
            self.apaga()

    def apaga(self):
        self.file = 'star2.png'
        self._acesa = False
    
    def acende(self):
        self.file = 'star.png'
        self._acesa = True

    def alterna(self):
        if self._acesa:
            self.apaga()
        else:
            self.acende()

    def estado(self):
        if self._acesa:
            return 'acesa'
        else:
            return 'apagada'


_label1 = Label('Chame os métodos do drone para capturar as estrelas', 5, 5)
drone = Drone()
item1 = Estrela(150, 250)
item2 = Estrela(250, 150)

run(globals())