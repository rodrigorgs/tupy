from tkfoot import *

class Carro(Objeto):
    def update(self):
        self.x += 1

class Star(Objeto):
    def __init__(self):
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
run(globals())
