import os
import sys
from typing import Optional
from PIL import ImageTk, Image as PILImage
import importlib.resources as pkg_resources
import random
import gettext
import tkinter.simpledialog as simpledialog

from tupy.gui import Window
from tupy.input_map import KeyboardMap, MouseMap
from tupy.inspector import inspector
from tupy.registry import Registry

_translation = gettext.translation('tupy', localedir=os.path.join(os.path.dirname(__file__), 'locale'), 
        languages=['en', 'pt_BR'])
_translation.install()

global_canvas = None
objects = Registry()
keyboard = KeyboardMap()
mouse = MouseMap()
_input = {
    'keyboard': keyboard,
    'mouse': mouse
}
window = Window(input=_input, common_supertype='tupy.TupyObject', registry=objects)

def input(prompt=''):
    variable = simpledialog.askstring(_('Text input'), prompt, parent=window.root)
    return variable

def toast(message, duration=3000):
    window.toast(message, duration)

def remove_public_members():
    for c in [TupyObject, BaseComposite, Image, Label, Rectangle, Oval]:
        for attr in dir(c):
            if not attr.startswith('_') and not attr == 'update':
                delattr(c, attr)
    # del Image.x
    # del Image.y
    # del Image.angle
    # del Image.file


class TupyObject:
    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        window.root.after(1, window.update_object_pane)
        # window.update_object_pane()
        return obj

    def _destroy(self):
        inspector.destroy_object(self)
        objects.remove_object(self)
        window.update_object_pane()
    destroy = _destroy

    def _hide(self):
        global_canvas.itemconfig(self._tkid, state='hidden')
    def _show(self):
        global_canvas.itemconfig(self._tkid, state='normal')

    def _position(self):
        return (self._x, self._y)

    def _contains_point(self, px, py):
        x, y = self._position()
        w, h = self._width / 2, self._height / 2
        return abs(x - px) < w and abs(y - py) < h

    def _collides_with(self, other):
        if not isinstance(other, TupyObject):
            raise TypeError('checking collision: other must be a tupy.Object')
        x, y = self._position()
        x, y = self._x, self._y
        w, h = self._width / 2, self._height / 2
        ox, oy = other._position()
        ow, oh = other._width / 2, other._height / 2
        return abs(x - ox) < w + ow and abs(y - oy) < h + oh

    @property
    def _top_left(self):
        return self._x, self._y
    
    def __str__(self) -> str:
        return f'<{self.__class__.__name__}:0x{id(self):02x}>'

class BaseComposite(TupyObject):
    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj._children = []
        return obj
    
    def _add(self, child):
        self._children.append(child)
    add = _add
    
    def _remove(self, child):
        self._children.remove(child)
    remove = _remove
    
    @property
    def children(self):
        return self._children

    @property
    def _x(self):
        if len(self._children) == 0:
            return 0
        else:
            return self._children[0]._x
    @_x.setter
    def _x(self, value):
        delta = value - self._x
        for child in self._children:
            child._x += delta
    x = _x

    @property
    def _y(self):
        if len(self._children) == 0:
            return 0
        else:
            return self._children[0]._y
    @_y.setter
    def _y(self, value):
        delta = value - self._y
        for child in self._children:
            child._y += delta
    y = _y

    def _hide(self):
        for child in self._children:
            child._hide()

    def _show(self):
        for child in self._children:
            child._show()

    def update(self):
        for child in self._children:
            if 'update' in dir(child):
                child.update()
    
    def _contains_point(self, px, py):
        return any(child._contains_point(px, py) for child in self._children)
    
    def _top_left(self):
        minx = min(child._top_left[0] for child in self._children)
        miny = min(child._top_left[1] for child in self._children)
        return minx, miny
    
    def _collides_with(self, other):
        return any(child._collides_with(other) for child in self._children)

class Oval(TupyObject):
    def __init__(self, x, y, width, height, outline='black', fill=''):
        self._tkid = global_canvas.create_oval(x, y, x+width, y+height, fill=fill, outline=outline)
        objects.add_object(self)
    
    @property
    def _x(self):
        return global_canvas.coords(self._tkid)[0]
    @_x.setter
    def _x(self, value):
        global_canvas.coords(self._tkid, value, self._y, self._x+self._width, self._y+self._height)
    x = _x
    @property
    def _y(self):
        return global_canvas.coords(self._tkid)[1]
    @_y.setter
    def _y(self, value):
        global_canvas.coords(self._tkid, self._x, value, self._x+self._width, self._y+self._height)
    y = _y
    @property
    def _width(self):
        return global_canvas.coords(self._tkid)[2] - self._x
    @_width.setter
    def _width(self, value):
        global_canvas.coords(self._tkid, self._x, self._y, self._x+value, self._y+self._height)
    width = _width
    @property
    def _height(self):
        return global_canvas.coords(self._tkid)[3] - self._y
    @_height.setter
    def _height(self, value):
        global_canvas.coords(self._tkid, self._x, self._y, self._x+self._width, self._y+value)
    height = _height
    @property
    def _fill(self):
        return global_canvas.itemcget(self._tkid, 'fill')
    @_fill.setter
    def _fill(self, value):
        global_canvas.itemconfig(self._tkid, fill=value)
    fill = _fill
    @property
    def _outline(self):
        return global_canvas.itemcget(self._tkid, 'outline')
    @_outline.setter
    def _outline(self, value):
        global_canvas.itemconfig(self._tkid, outline=value)
    outline = _outline

    def destroy(self):
        global_canvas.delete(self._tkid)

class Label(TupyObject):
    def __init__(self, text, x, y, font='Arial 20', color='black', anchor='nw'):
        self._tkid = global_canvas.create_text(x, y, text=text, font=font, fill=color, anchor=anchor)
        objects.add_object(self)
    
    @property
    def _x(self):
        return global_canvas.coords(self._tkid)[0]
    @_x.setter
    def _x(self, value):
        global_canvas.coords(self._tkid, value, self._y)
    x = _x
    @property
    def _y(self):
        return global_canvas.coords(self._tkid)[1]
    @_y.setter
    def _y(self, value):
        global_canvas.coords(self._tkid, self._x, value)
    y = _y
    @property
    def _text(self):
        return global_canvas.itemcget(self._tkid, 'text')
    @_text.setter
    def _text(self, value):
        global_canvas.itemconfig(self._tkid, text=value)
    text = _text
    @property
    def _font(self):
        return global_canvas.itemcget(self._tkid, 'font')
    @_font.setter
    def _font(self, value):
        global_canvas.itemconfig(self._tkid, font=value)
    font = _font
    @property
    def _color(self):
        return global_canvas.itemcget(self._tkid, 'fill')
    @_color.setter
    def _color(self, value):
        global_canvas.itemconfig(self._tkid, fill=value)
    color = _color
    @property
    def _width(self):
        return global_canvas.bbox(self._tkid)[2] - self._x
    @property
    def _height(self):
        return global_canvas.bbox(self._tkid)[3] - self._y
    @property
    def _anchor(self):
        return global_canvas.itemcget(self._tkid, 'anchor')
    @_anchor.setter
    def _anchor(self, value):
        global_canvas.itemconfig(self._tkid, anchor=value)
    anchor = _anchor

class Rectangle(TupyObject):
    def __init__(self, x, y, w, h, outline='black', fill=''):
        self._tkid = global_canvas.create_rectangle(x, y, x + w, y + h, outline=outline, fill=fill)
        objects.add_object(self)

    @property
    def _x(self):
        return global_canvas.coords(self._tkid)[0]
    @_x.setter
    def _x(self, value):
        global_canvas.coords(self._tkid, value, self._y, value + self._width, self._y + self._height)
    x = _x
    @property
    def _y(self):
        return global_canvas.coords(self._tkid)[1]
    @_y.setter
    def _y(self, value):
        global_canvas.coords(self._tkid, self._x, value, self._x + self._width, value + self._height)
    y = _y
    @property
    def _width(self):
        return global_canvas.coords(self._tkid)[2] - self._x
    @_width.setter
    def _width(self, value):
        global_canvas.coords(self._tkid, self._x, self._y, self._x + value, self._y + self._height)
    width = _width
    @property
    def _height(self):
        return global_canvas.coords(self._tkid)[3] - self._y
    @_height.setter
    def _height(self, value):
        global_canvas.coords(self._tkid, self._x, self._y, self._x + self._width, self._y + value)
    height = _height
    @property
    def _fill(self):
        return global_canvas.itemcget(self._tkid, 'fill')
    @_fill.setter
    def _fill(self, value):
        global_canvas.itemconfig(self._tkid, fill=value)
    fill = _fill
    @property
    def _outline(self):
        return global_canvas.itemcget(self._tkid, 'outline')
    @_outline.setter
    def _outline(self, value):
        global_canvas.itemconfig(self._tkid, outline=value)
    outline = _outline

class PrivateImageAttributes:
    def __init__(self) -> None:
        self.file = ''
        self.angle = 0

class BaseImage(TupyObject):
    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        self._attrs = PrivateImageAttributes()
        x = random.randint(0, Window.CANVAS_WIDTH)
        y = random.randint(0, Window.CANVAS_HEIGHT)
        self._initialize(x, y)
        return self

    def _initialize(self, x, y):
        # if self._image_path is None:
        self._attrs.file = self.__class__.__name__.lower() + '.png'
        self._image_path = self._find_image_path(self._file)
        self._tkobject = ImageTk.PhotoImage(PILImage.open(self._image_path))
        self._tkid = global_canvas.create_image(x, y, image=self._tkobject)
        objects.add_object(self)

    @property
    def _top_left(self):
        return self._x - self._width / 2, self._y - self._height / 2

    @property
    def _x(self):
        return global_canvas.coords(self._tkid)[0]
    @_x.setter
    def _x(self, value):
        global_canvas.coords(self._tkid, value, self._y)
    @property
    def _y(self):
        return global_canvas.coords(self._tkid)[1]
    @_y.setter
    def _y(self, value):
        global_canvas.coords(self._tkid, self._x, value)
    @property
    def _width(self):
        return self._tkobject.width()
    @property
    def _height(self):
        return self._tkobject.height()
    
    
    @property
    def _angle(self):
        return self._attrs.angle
    @_angle.setter
    def _angle(self, value):
        self._attrs.angle = value
        self._tkobject = ImageTk.PhotoImage(PILImage.open(self._image_path).rotate(value))
        global_canvas.itemconfig(self._tkid, image=self._tkobject)

    @property
    def _file(self):
        return self._attrs.file
        
    @_file.setter
    def _file(self, value):
        self._attrs.file = value
        self._image_path = self._find_image_path(value)
        self._tkobject = ImageTk.PhotoImage(PILImage.open(self._image_path))
        global_canvas.itemconfig(self._tkid, image=self._tkobject)
        self._angle = self._angle # Rotate image if needed

    def _find_image_path(self, filename):
        script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
        path = os.path.join(script_dir, filename)
        if not os.path.exists(path):
            path = path = os.path.join(script_dir, "assets", filename)
        if not os.path.exists(path):
            with pkg_resources.path('tupy', 'assets') as pkg_path:
                path = os.path.join(pkg_path, filename)
        if not os.path.exists(path):
            with pkg_resources.path('tupy', 'assets') as pkg_path:
                path = os.path.join(pkg_path, 'missing.png')
        return path

class Image(BaseImage):
    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        return self

    x = BaseImage._x
    y = BaseImage._y
    file = BaseImage._file
    angle = BaseImage._angle

# global global_canvas
window.create()
global_canvas = window.canvas

def run(globals):
    inspector.env = globals
    window._inspector = inspector
    window.update_object_pane()
    window.main_loop()
