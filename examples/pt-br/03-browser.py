from tupy import *

class Star(Image):
    def __init__(self) -> None:
        super().__init__()
    
    def update(self):
        self.angle = (self.angle + 5) % 360

class Drone(Image):
    def __init__(self) -> None:
        super().__init__()
        self.stars = []
        self.stars.append(Star())
        self.stars.append(Star())
        self.stars.append(Star())
        self.tuple = (1, 2, 3)
        self.dict = {'a': 1, 'b': 2, 'c': 3}

drone = Drone()

def update():
    for x in drone.stars:
        x.update()

run(globals())