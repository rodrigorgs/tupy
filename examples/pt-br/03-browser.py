from tupy import *

class Star(Image):
    def __init__(self) -> None:
        super().__init__()

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

run(globals())