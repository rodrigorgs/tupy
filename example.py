from tkfoot import *

class Carro(Object):
    def update(self):
        self.x += 1

class Star(Object):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.contador = 10
        self.ativado = True
    
    def desativar(self):
        self.image = 'star2.png'
        self.ativado = False
    def ativar(self):
        self.image = 'star.png'
        self.ativado = True
    def update(self):
        self.contador -= 1
        if self.contador == 0:
            self.contador = 10
            if self.ativado:
                self.desativar()
            else:
                self.ativar()

carro = Carro()
star = Star()
star.x = 100
star.y = 100
a = Star(20, 20)
b = Star(50, 50)
c = Star(20, 50)
d = Star(50, 20)

run(globals())
