from typing import Optional
from inspector import Inspector
from gui import Window
from PIL import ImageTk, Image

canvas = None
inspector = None

class Object:
    def __init__(self):
        self._image_path = self.__class__.__name__.lower() + '.png'
        self._img = ImageTk.PhotoImage(Image.open(self._image_path))
        self._sprite = canvas.create_image(50, 50, image=self._img)
        print('objeto init')
        print(type(self._sprite))

    def destroy(self):
        inspector.destroy_object(self)

    @property
    def x(self):
        return canvas.coords(self._sprite)[0]

    @x.setter
    def x(self, value):
        canvas.coords(self._sprite, value, self.y)

    @property
    def y(self):
        return canvas.coords(self._sprite)[1]

    @y.setter
    def y(self, value):
        canvas.coords(self._sprite, self.x, value)

    @property
    def image(self):
        return self._image_path
    @image.setter
    def image(self, value):
        self._image_path = value
        self._img = ImageTk.PhotoImage(Image.open(self._image_path))
        canvas.itemconfig(self._sprite, image=self._img)

window = Window(inspector=inspector, common_supertype=Object)
window.create()
canvas = window.canvas

def run(globals):
    global inspector
    inspector = Inspector(globals)
    window._inspector = inspector
    window.update_object_pane()
    window.main_loop()
