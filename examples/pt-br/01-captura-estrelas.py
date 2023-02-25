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
        if drone.collides_with(item):
            item.acende()
        else:
            item.apaga()

class Star(Image):
    pass

class Estrela(Image):
    def __init__(self):
        self.path = 'star2.png'
        self.x = 150
        self.y = 250
        self._acesa = False

    def apaga(self):
        self.path = 'star2.png'
        self._acesa = False
    
    def acende(self):
        self.path = 'star.png'
        self._acesa = True

    def estado(self):
        if self._acesa:
            return 'acesa'
        else:
            return 'apagada'


drone = Drone()
item = Estrela()

run(globals())