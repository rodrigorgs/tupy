from tupy import *

class Drone(Image):
    def update(self):
        if input.is_key_down('Right'):
            self.x += 10
        if input.is_key_down('Left'):
            self.x -= 10
        if input.is_key_down('Up'):
            self.y -= 10
        if input.is_key_down('Down'):
            self.y += 10

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

if __name__ == '__main__':
    drone = Drone()
    star1 = Star()
    star2 = Star()
    star3 = Star()
    star4 = Star()

    rect = Rectangle(0, 0, 640, 40, fill='lightgray', outline='')
    circle = Oval(5, 5, 30, 30, fill='darkgreen', outline='')
    score = Score()

    run(globals())