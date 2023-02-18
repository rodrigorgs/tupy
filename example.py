import tupy

class Carro(tupy.Object):
    def __init__(self):
        super().__init__()
        self.stars = []

    def update(self):
        if self._input.is_key_down('Right'):
            self.x += 10
        if self._input.is_key_down('Left'):
            self.x -= 10
        if self._input.is_key_just_down('Up'):
            self.angle += 45
        if self._input.is_key_just_down('space'):
            self.dispara()
        for s in self.stars:
            s.update()

    def dispara(self):
        s = Star()
        s.x = self.x
        s.y = self.y
        self.stars.append(s)

    def reinicia(self):
        self.x = 100
        for s in self.stars:
            s.destroy()
        self.stars = []

class Star(tupy.Object):
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
        self.angle = (self.angle + 10) % 360
        self.contador -= 1
        if self.contador == 0:
            self.contador = 10
            if self.ativado:
                self.desativar()
            else:
                self.ativar()

carro = Carro()
carro.y = 200
star = Star()
star.x = 100
star.y = 400
# a = Star(20, 20)
# b = Star(50, 50)
# c = Star(20, 50)
# d = Star(50, 20)

tupy.run(globals())
