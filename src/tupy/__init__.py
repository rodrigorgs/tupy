from typing import Optional
from PIL import ImageTk, Image

from tupy.gui import Window
from tupy.input import InputMap
from tupy.inspector import Inspector

global_canvas = None
inspector: Optional[Inspector] = None
input = InputMap()

class Object:
    def __init__(self):
        self._image_path = self.__class__.__name__.lower() + '.png'
        self._img = ImageTk.PhotoImage(Image.open(self._image_path))
        self._sprite = global_canvas.create_image(50, 50, image=self._img)
        self._angle = 0
        self._input = input

    def collides_with(self, other):
        if not isinstance(other, Object):
            raise TypeError('checking collision: other must be a tupy.Object')
        x, y = self.x, self.y
        w, h = self._img.width() / 2, self._img.height() / 2
        ox, oy = other.x, other.y
        ow, oh = other._img.width() / 2, other._img.height() / 2
        return abs(x - ox) < w + ow and abs(y - oy) < h + oh

    def destroy(self):
        inspector.destroy_object(self)

    @property
    def x(self):
        return global_canvas.coords(self._sprite)[0]

    @x.setter
    def x(self, value):
        global_canvas.coords(self._sprite, value, self.y)

    @property
    def y(self):
        return global_canvas.coords(self._sprite)[1]

    @y.setter
    def y(self, value):
        global_canvas.coords(self._sprite, self.x, value)

    @property
    def image(self):
        return self._image_path
    @image.setter
    def image(self, value):
        self._image_path = value
        self._img = ImageTk.PhotoImage(Image.open(self._image_path))
        global_canvas.itemconfig(self._sprite, image=self._img)
        self.angle = self.angle # Rotate image if needed

    @property
    def angle(self):
        return self._angle
    @angle.setter
    def angle(self, value):
        self._angle = value
        self._img = ImageTk.PhotoImage(Image.open(self._image_path).rotate(value))
        global_canvas.itemconfig(self._sprite, image=self._img)

window = Window(inspector=inspector, input=input, common_supertype=Object)
window.create()
global_canvas = window.canvas

def run(globals):
    global inspector
    inspector = Inspector(globals)
    window._inspector = inspector
    window.update_object_pane()
    window.main_loop()
