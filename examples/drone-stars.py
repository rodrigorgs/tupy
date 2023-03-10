from tupy import *

class Drone(Image):
    def update(self):
        if Input.is_key_down('Right'):
            self.x += 10
        if Input.is_key_down('Left'):
            self.x -= 10
        if Input.is_key_down('Up'):
            self.y -= 10
        if Input.is_key_down('Down'):
            self.y += 10

        if Input.is_key_just_down('space'):
            global star1
            star1 = Star()
            star1.x = self.x + 100
            star1.y = self.y + 100

        if Input.is_mouse_just_down():
            self.x = Input.mouse_x
            self.y = Input.mouse_y

class Star(Image):
    def update(self):
        self.angle = (self.angle + 5) % 360
        if self.collides_with(drone):
            self.destroy()
            score.increment()

class Score(Label):
    def __init__(self) -> None:
        super().__init__('Score: 0', 40, 9, font='Arial 20')
        self.score = 0
    
    def increment(self):
        self.score += 1
        self.text = f'Score: {self.score}'

    def update(self):
        coords.text = f'{Input.mouse_x}, {Input.mouse_y}'

if __name__ == '__main__':
    drone = Drone()
    star1 = Star()
    star2 = Star()
    star3 = Star()
    star4 = Star()

    rect = Rectangle(0, 0, 640, 40, fill='lightgray', outline='')
    circle = Oval(5, 5, 30, 30, fill='darkgreen', outline='')
    score = Score()
    coords = Label('0, 0', 300, 9, font='Arial 20')

    run(globals())