from tkfoot import *

class Carro(Objeto):
    def update(self):
        self.x += 1

carro = Carro()
run(globals())
