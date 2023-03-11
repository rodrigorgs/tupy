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


drone = Drone()

run(globals())