from tupy import *

class Player(BaseImage):
    SPEED = 10
    
    def __init__(self) -> None:
        self._file = 'star.png'
        self._shadow = Image('star2.png', self._x + 5, self._y + 5)

    def update(self) -> None:
        self._shadow.x = self._x + 5
        self._shadow.y = self._y + 5
        self._shadow.angle = self._angle
        self._angle = (self._angle + 5) % 360

        if keyboard.is_key_down('Up'):
            self._y -= self.SPEED
        if keyboard.is_key_down('Down'):
            self._y += self.SPEED
        if keyboard.is_key_down('Left'):
            self._x -= self.SPEED
        if keyboard.is_key_down('Right'):
            self._x += self.SPEED

class Face(BaseComposite):
    pass

class Placar(BaseComposite):
    def __init__(self) -> None:
        self.pontos = 0
        self._add(Rectangle(0, 0, Window.CANVAS_WIDTH, 40, fill='lightgray', outline='darkgray'))
        
        self._label_mouse = Label('Mova o mouse', 5, 5, font='Arial 20', color='black')
        self._add(self._label_mouse)
    
    def update(self) -> None:
        super().update()
        self._label_mouse.text = f'Mouse: {mouse.x}, {mouse.y}, {mouse.is_button_down()}. Pontos: {self.pontos}'
        if keyboard.is_key_just_down('space'):
            self.pontuar()

    def pontuar(self) -> None:
        self.pontos += 15

placar = Placar()
player = Player()

run(globals())