from tupy import *

class Star(Image):
    def update(self):
        self.x += 5
        if self.x > 640:
            self.x = 0

class Tiro(Image):
    def __init__(self):
        self.file = 'ball.png'

    def update(self):
        self.y -= 15
        if self._collides_with(inimigo):
            inimigo.destroy()

class Smiley(Image):
    def __init__(self):
        self.tiro = None

    def update(self):
        if keyboard.is_key_just_down('space'):
            self.dispara()
        if self.tiro is not None:
            self.tiro.update()
            if self.tiro.y < -10:
                self.tiro.destroy()
                self.tiro = None
    
    def dispara(self):
        self.tiro = Tiro()
        self.tiro.x = self.x
        self.tiro.y = self.y

inimigo = Star()
inimigo.x = 0
inimigo.y = 50

player = Smiley()
player.x = 320
player.y = 450

run(globals())