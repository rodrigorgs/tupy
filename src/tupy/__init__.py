from typing import Optional
from PIL import ImageTk, Image as PILImage
import importlib.resources as pkg_resources
import os
import random

from tupy.gui import Window
from tupy.input import InputMap
from tupy.inspector import Inspector

global_canvas = None
inspector: Optional[Inspector] = None
input = InputMap()

class TupyObject:
    def destroy(self):
        inspector.destroy_object(self)

    def collides_with(self, other):
        if not isinstance(other, TupyObject):
            raise TypeError('checking collision: other must be a tupy.Object')
        x, y = self.x, self.y
        w, h = self.width / 2, self.height / 2
        ox, oy = other.x, other.y
        ow, oh = other.width / 2, other.height / 2
        return abs(x - ox) < w + ow and abs(y - oy) < h + oh

    @property
    def _top_left(self):
        return self.x, self.y

class Oval(TupyObject):
    def __init__(self, x, y, width, height, outline='black', fill=''):
        self._tkobject = global_canvas.create_oval(x, y, x+width, y+height, fill=fill, outline=outline)
    
    @property
    def x(self):
        return global_canvas.coords(self._tkobject)[0]
    @x.setter
    def x(self, value):
        global_canvas.coords(self._tkobject, value, self.y, self.x+self.width, self.y+self.height)
    @property
    def y(self):
        return global_canvas.coords(self._tkobject)[1]
    @y.setter
    def y(self, value):
        global_canvas.coords(self._tkobject, self.x, value, self.x+self.width, self.y+self.height)
    @property
    def width(self):
        return global_canvas.coords(self._tkobject)[2] - self.x
    @width.setter
    def width(self, value):
        global_canvas.coords(self._tkobject, self.x, self.y, self.x+value, self.y+self.height)
    @property
    def height(self):
        return global_canvas.coords(self._tkobject)[3] - self.y
    @height.setter
    def height(self, value):
        global_canvas.coords(self._tkobject, self.x, self.y, self.x+self.width, self.y+value)
    @property
    def fill(self):
        return global_canvas.itemcget(self._tkobject, 'fill')
    @fill.setter
    def fill(self, value):
        global_canvas.itemconfig(self._tkobject, fill=value)
    @property
    def outline(self):
        return global_canvas.itemcget(self._tkobject, 'outline')
    @outline.setter
    def outline(self, value):
        global_canvas.itemconfig(self._tkobject, outline=value)
    
    def destroy(self):
        global_canvas.delete(self._tkobject)

class Label(TupyObject):
    def __init__(self, text, x, y, font='Arial 10', color='black', anchor='nw'):
        self._tkobject = global_canvas.create_text(x, y, text=text, font=font, fill=color, anchor=anchor)
    
    @property
    def x(self):
        return global_canvas.coords(self._tkobject)[0]
    @x.setter
    def x(self, value):
        global_canvas.coords(self._tkobject, value, self.y)
    @property
    def y(self):
        return global_canvas.coords(self._tkobject)[1]
    @y.setter
    def y(self, value):
        global_canvas.coords(self._tkobject, self.x, value)
    @property
    def text(self):
        return global_canvas.itemcget(self._tkobject, 'text')
    @text.setter
    def text(self, value):
        global_canvas.itemconfig(self._tkobject, text=value)
    @property
    def font(self):
        return global_canvas.itemcget(self._tkobject, 'font')
    @font.setter
    def font(self, value):
        global_canvas.itemconfig(self._tkobject, font=value)
    @property
    def color(self):
        return global_canvas.itemcget(self._tkobject, 'fill')
    @color.setter
    def color(self, value):
        global_canvas.itemconfig(self._tkobject, fill=value)
    @property
    def width(self):
        return global_canvas.bbox(self._tkobject)[2] - self.x
    @property
    def height(self):
        return global_canvas.bbox(self._tkobject)[3] - self.y
    @property
    def anchor(self):
        return global_canvas.itemcget(self._tkobject, 'anchor')
    @anchor.setter
    def anchor(self, value):
        global_canvas.itemconfig(self._tkobject, anchor=value)

class Rectangle(TupyObject):
    def __init__(self, x, y, w, h, outline='black', fill=''):
        self._tkobject = global_canvas.create_rectangle(10, 10, 50, 50, fill='black')

    @property
    def x(self):
        return global_canvas.coords(self._tkobject)[0]
    @x.setter
    def x(self, value):
        global_canvas.coords(self._tkobject, value, self.y, value + self.width, self.y + self.height)
    @property
    def y(self):
        return global_canvas.coords(self._tkobject)[1]
    @y.setter
    def y(self, value):
        global_canvas.coords(self._tkobject, self.x, value, self.x + self.width, value + self.height)
    @property
    def width(self):
        return global_canvas.coords(self._tkobject)[2] - self.x
    @width.setter
    def width(self, value):
        global_canvas.coords(self._tkobject, self.x, self.y, self.x + value, self.y + self.height)
    @property
    def height(self):
        return global_canvas.coords(self._tkobject)[3] - self.y
    @height.setter
    def height(self, value):
        global_canvas.coords(self._tkobject, self.x, self.y, self.x + self.width, self.y + value)
    @property
    def fill(self):
        return global_canvas.itemcget(self._tkobject, 'fill')
    @fill.setter
    def fill(self, value):
        global_canvas.itemconfig(self._tkobject, fill=value)
    @property
    def outline(self):
        return global_canvas.itemcget(self._tkobject, 'outline')
    @outline.setter
    def outline(self, value):
        global_canvas.itemconfig(self._tkobject, outline=value)

class Image(TupyObject):
    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        # self._image_path = path
        x = random.randint(0, Window.CANVAS_WIDTH)
        y = random.randint(0, Window.CANVAS_HEIGHT)
        self._initialize(x, y)
        return self

    def _initialize(self, x, y):
        # if self._image_path is None:
        self._image_path = self._find_image_path(self.__class__.__name__.lower() + '.png')
        if not os.path.exists(self._image_path):
            self._image_path = os.path.join(pkg_resources.path('tupy', 'assets'), self._image_path)
        if not os.path.exists(self._image_path):
            self._image_path = os.path.join(pkg_resources.path('tupy', 'assets'), 'missing.png')
        self._tkobject = ImageTk.PhotoImage(PILImage.open(self._image_path))

        self._sprite = global_canvas.create_image(x, y, image=self._tkobject)
        self._angle = 0
        self._input = input

    @property
    def _top_left(self):
        return self.x - self.width / 2, self.y - self.height / 2

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
    def width(self):
        return self._tkobject.width()
    @property
    def height(self):
        return self._tkobject.height()

    @property
    def path(self):
        return self._image_path
    @path.setter
    def path(self, value):
        self._image_path = self._find_image_path(value)
        self._tkobject = ImageTk.PhotoImage(PILImage.open(self._image_path))
        global_canvas.itemconfig(self._sprite, image=self._tkobject)
        self.angle = self.angle # Rotate image if needed

    def _find_image_path(self, path):
        if not os.path.exists(path):
            path = os.path.join(pkg_resources.path('tupy', 'assets'), path)
        if not os.path.exists(path):
            path = os.path.join(pkg_resources.path('tupy', 'assets'), 'missing.png')
        return path


    @property
    def angle(self):
        return self._angle
    @angle.setter
    def angle(self, value):
        self._angle = value
        self._tkobject = ImageTk.PhotoImage(PILImage.open(self._image_path).rotate(value))
        global_canvas.itemconfig(self._sprite, image=self._tkobject)

window = Window(inspector=inspector, input=input, common_supertype=TupyObject)
window.create()
global_canvas = window.canvas

def run(globals):
    global inspector
    inspector = Inspector(globals)
    window._inspector = inspector
    window.update_object_pane()
    window.main_loop()
