import os
from typing import Optional
from PIL import ImageTk, Image as PILImage
import importlib.resources as pkg_resources
import os
import random
import gettext

from tupy.gui import Window
from tupy.input_map import InputMap
from tupy.inspector import inspector
from tupy.registry import Registry

_translation = gettext.translation('tupy', localedir=os.path.join(os.path.dirname(__file__), 'locale'), 
        languages=['en', 'pt_BR'])
_translation.install()

global_canvas = None
objects = Registry()
input = InputMap()
window = Window(input=input, common_supertype='tupy.TupyObject', registry=objects)

class TupyObject:
    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        window.root.after(1, window.update_object_pane)
        # window.update_object_pane()
        return obj

    def destroy(self):
        inspector.destroy_object(self)
        objects.remove_object(self)
        window.update_object_pane()

    def _contains_point(self, px, py):
        x, y = self.x, self.y
        w, h = self._width / 2, self._height / 2
        return abs(x - px) < w and abs(y - py) < h

    def collides_with(self, other):
        if not isinstance(other, TupyObject):
            raise TypeError('checking collision: other must be a tupy.Object')
        x, y = self.x, self.y
        w, h = self._width / 2, self._height / 2
        ox, oy = other.x, other.y
        ow, oh = other._width / 2, other._height / 2
        return abs(x - ox) < w + ow and abs(y - oy) < h + oh

    @property
    def _top_left(self):
        return self.x, self.y
    
    def __str__(self) -> str:
        return f'<{self.__class__.__name__}:0x{id(self):02x}>'

class Oval(TupyObject):
    def __init__(self, x, y, width, height, outline='black', fill=''):
        self._tkid = global_canvas.create_oval(x, y, x+width, y+height, fill=fill, outline=outline)
        objects.add_object(self)
    
    @property
    def x(self):
        return global_canvas.coords(self._tkid)[0]
    @x.setter
    def x(self, value):
        global_canvas.coords(self._tkid, value, self.y, self.x+self._width, self.y+self._height)
    @property
    def y(self):
        return global_canvas.coords(self._tkid)[1]
    @y.setter
    def y(self, value):
        global_canvas.coords(self._tkid, self.x, value, self.x+self._width, self.y+self._height)
    @property
    def _width(self):
        return global_canvas.coords(self._tkid)[2] - self.x
    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, value):
        global_canvas.coords(self._tkid, self.x, self.y, self.x+value, self.y+self._height)
    @property
    def _height(self):
        return global_canvas.coords(self._tkid)[3] - self.y
    @property
    def height(self):
        return self._height
    @height.setter
    def height(self, value):
        global_canvas.coords(self._tkid, self.x, self.y, self.x+self._width, self.y+value)
    @property
    def fill(self):
        return global_canvas.itemcget(self._tkid, 'fill')
    @fill.setter
    def fill(self, value):
        global_canvas.itemconfig(self._tkid, fill=value)
    @property
    def outline(self):
        return global_canvas.itemcget(self._tkid, 'outline')
    @outline.setter
    def outline(self, value):
        global_canvas.itemconfig(self._tkid, outline=value)
    
    def destroy(self):
        global_canvas.delete(self._tkid)

class Label(TupyObject):
    def __init__(self, text, x, y, font='Arial 20', color='black', anchor='nw'):
        self._tkid = global_canvas.create_text(x, y, text=text, font=font, fill=color, anchor=anchor)
        objects.add_object(self)
    
    @property
    def x(self):
        return global_canvas.coords(self._tkid)[0]
    @x.setter
    def x(self, value):
        global_canvas.coords(self._tkid, value, self.y)
    @property
    def y(self):
        return global_canvas.coords(self._tkid)[1]
    @y.setter
    def y(self, value):
        global_canvas.coords(self._tkid, self.x, value)
    @property
    def text(self):
        return global_canvas.itemcget(self._tkid, 'text')
    @text.setter
    def text(self, value):
        global_canvas.itemconfig(self._tkid, text=value)
    @property
    def font(self):
        return global_canvas.itemcget(self._tkid, 'font')
    @font.setter
    def font(self, value):
        global_canvas.itemconfig(self._tkid, font=value)
    @property
    def color(self):
        return global_canvas.itemcget(self._tkid, 'fill')
    @color.setter
    def color(self, value):
        global_canvas.itemconfig(self._tkid, fill=value)
    @property
    def _width(self):
        return global_canvas.bbox(self._tkid)[2] - self.x
    @property
    def _height(self):
        return global_canvas.bbox(self._tkid)[3] - self.y
    @property
    def anchor(self):
        return global_canvas.itemcget(self._tkid, 'anchor')
    @anchor.setter
    def anchor(self, value):
        global_canvas.itemconfig(self._tkid, anchor=value)

class Rectangle(TupyObject):
    def __init__(self, x, y, w, h, outline='black', fill=''):
        self._tkid = global_canvas.create_rectangle(x, y, x + w, y + h, outline=outline, fill=fill)
        objects.add_object(self)

    @property
    def x(self):
        return global_canvas.coords(self._tkid)[0]
    @x.setter
    def x(self, value):
        global_canvas.coords(self._tkid, value, self.y, value + self._width, self.y + self._height)
    @property
    def y(self):
        return global_canvas.coords(self._tkid)[1]
    @y.setter
    def y(self, value):
        global_canvas.coords(self._tkid, self.x, value, self.x + self._width, value + self._height)
    @property
    def _width(self):
        return global_canvas.coords(self._tkid)[2] - self.x
    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, value):
        global_canvas.coords(self._tkid, self.x, self.y, self.x + value, self.y + self._height)
    @property
    def _height(self):
        return global_canvas.coords(self._tkid)[3] - self.y
    @property
    def height(self):
        return self._height
    @height.setter
    def height(self, value):
        global_canvas.coords(self._tkid, self.x, self.y, self.x + self._width, self.y + value)
    @property
    def fill(self):
        return global_canvas.itemcget(self._tkid, 'fill')
    @fill.setter
    def fill(self, value):
        global_canvas.itemconfig(self._tkid, fill=value)
    @property
    def outline(self):
        return global_canvas.itemcget(self._tkid, 'outline')
    @outline.setter
    def outline(self, value):
        global_canvas.itemconfig(self._tkid, outline=value)

class Image(TupyObject):
    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        x = random.randint(0, Window.CANVAS_WIDTH)
        y = random.randint(0, Window.CANVAS_HEIGHT)
        self._initialize(x, y)
        return self

    def _initialize(self, x, y):
        # if self._image_path is None:
        self._file = self.__class__.__name__.lower() + '.png'
        self._image_path = self._find_image_path(self._file)
        self._tkobject = ImageTk.PhotoImage(PILImage.open(self._image_path))

        self._tkid = global_canvas.create_image(x, y, image=self._tkobject)
        self._angle = 0
        self._input = input

        objects.add_object(self)

    @property
    def _top_left(self):
        return self.x - self._width / 2, self.y - self._height / 2

    @property
    def x(self):
        return global_canvas.coords(self._tkid)[0]

    @x.setter
    def x(self, value):
        global_canvas.coords(self._tkid, value, self.y)

    @property
    def y(self):
        return global_canvas.coords(self._tkid)[1]

    @y.setter
    def y(self, value):
        global_canvas.coords(self._tkid, self.x, value)

    @property
    def _width(self):
        return self._tkobject.width()
    @property
    def _height(self):
        return self._tkobject.height()

    @property
    def file(self):
        return self._file
        
    @file.setter
    def file(self, value):
        self._file = value
        self._image_path = self._find_image_path(value)
        self._tkobject = ImageTk.PhotoImage(PILImage.open(self._image_path))
        global_canvas.itemconfig(self._tkid, image=self._tkobject)
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
        global_canvas.itemconfig(self._tkid, image=self._tkobject)

# global global_canvas
window.create()
global_canvas = window.canvas

def run(globals):
    inspector.env = globals
    window._inspector = inspector
    window.update_object_pane()
    window.main_loop()
