from tupy import *

class Star(Image):
    SPEED = 10
    def __init__(self) -> None:
        self.label = Label('x 0 y 0 button False', 20, 20)
    def update(self):
        self.label.text = f'x {mouse.x} y {mouse.y} button {mouse.is_button_down()}'
        if keyboard.is_key_down('Up'):
            self.y -= 10
        if keyboard.is_key_down('Down'):
            self.y += 10
        if keyboard.is_key_down('Left'):
            self.x -= 10
        if keyboard.is_key_down('Right'):
            self.x += 10

s = Star()

run(globals())