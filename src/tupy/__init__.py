import os
import sys
from typing import Any, Literal, Optional, cast
from PIL import ImageTk, Image as PILImage
import importlib.resources as pkg_resources
import random
import tkinter.simpledialog as simpledialog
from tupy.translation import _

from tupy.gui import Window
from tupy.input_map import KeyboardMap, MouseMap
from tupy.inspector import inspector
from tupy.registry import Registry
from tupy.tupyobject import TupyObject

# _translation.install()

objects = Registry()
keyboard = KeyboardMap()
mouse = MouseMap()
window = Window(keyboard=keyboard, mouse=mouse, registry=objects)

def input(prompt: str = '') -> Optional[str]:
    variable = simpledialog.askstring(_('Text input'), prompt, parent=window.root)
    return variable

def toast(message: str, duration: int = 3000) -> None:
    window.toast(message, duration)

def remove_public_members() -> None:
    for c in [TupyObject, BaseGroup, Image, Label, Rectangle, Oval]:
        for attr in dir(c):
            if not attr.startswith('_') and not attr == 'update':
                delattr(c, attr)
    # del Image.x
    # del Image.y
    # del Image.angle
    # del Image.file


class BaseTupyObject(TupyObject):
    def __new__(cls, *args: Any, **kwargs: Any) -> 'BaseTupyObject':
        obj = super().__new__(cls)
        window.root.after(1, window.update_object_pane)
        # window.update_object_pane()
        return obj

    def _destroy(self) -> None:
        inspector.destroy_object(self)
        objects.remove_object(self)
        window.update_object_pane()
    def destroy(self) -> None:
        self._destroy()

    def _hide(self) -> None:
        window.canvas.itemconfig(self._tkid, state='hidden')
    def _show(self) -> None:
        window.canvas.itemconfig(self._tkid, state='normal')

    def _position(self) -> tuple[int, int]:
        return (self._x, self._y)

    def _contains_point(self, px: int, py: int) -> bool:
        x, y = self._position()
        w, h = self._width / 2, self._height / 2
        return abs(x - px) < w and abs(y - py) < h

    def _collides_with(self, other: TupyObject) -> bool:
        if not isinstance(other, TupyObject):
            raise TypeError('checking collision: other must be a tupy.Object')
        x, y = self._position()
        x, y = self._x, self._y
        w, h = self._width / 2, self._height / 2
        ox, oy = other._position()
        ow, oh = other._width / 2, other._height / 2
        return abs(x - ox) < w + ow and abs(y - oy) < h + oh

    @property
    def _top_left(self) -> tuple[int, int]:
        return self._x, self._y
    
    def update(self) -> None:
        pass

    def __str__(self) -> str:
        return f'<{self.__class__.__name__}:0x{id(self):02x}>'

class BaseGroup(BaseTupyObject):
    _children_objs: list[TupyObject]
    _tkid: int

    def __new__(cls, *args: Any, **kwargs: Any) -> 'BaseGroup':
        obj = super().__new__(cls)
        setattr(obj, '_children_objs', [])
        setattr(obj, '_tkid', -1)
        return cast('BaseGroup', obj)
    
    def _add(self, child: TupyObject) -> None:
        self._children_objs.append(child)
    
    def _remove(self, child: TupyObject) -> None:
        self._children_objs.remove(child)
    
    def _clear(self) -> None:
        self._children_objs.clear()

    @property
    def _objects(self) -> list[TupyObject]:
        return [*self._children_objs]

    @property
    def _x(self) -> int:
        if len(self._children_objs) == 0:
            return 0
        else:
            return self._children_objs[0]._x
    @_x.setter
    def _x(self, value: int) -> None:
        delta = value - self._x
        for child in self._children_objs:
            child._x += delta

    @property
    def _y(self) -> int:
        if len(self._children_objs) == 0:
            return 0
        else:
            return self._children_objs[0]._y
    @_y.setter
    def _y(self, value: int) -> None:
        delta = value - self._y
        for child in self._children_objs:
            child._y += delta

    def _hide(self) -> None:
        for child in self._children_objs:
            child._hide()

    def _show(self) -> None:
        for child in self._children_objs:
            child._show()

    def update(self) -> None:
        for child in self._children_objs:
            if 'update' in dir(child):
                child.update()
    
    def _contains_point(self, px: int, py: int) -> bool:
        return any(child._contains_point(px, py) for child in self._children_objs)
    
    @property
    def _top_left(self) -> tuple[int, int]:
        minx = min(child._top_left[0] for child in self._children_objs)
        miny = min(child._top_left[1] for child in self._children_objs)
        return minx, miny
    
    def _collides_with(self, other: TupyObject) -> bool:
        return any(child._collides_with(other) for child in self._children_objs)

class Group(BaseGroup):
    x = cast(property, BaseGroup._x)
    y = cast(property, BaseGroup._y)
    objects = cast(property, BaseGroup._objects)
    add = cast(property, BaseGroup._add)
    remove = cast(property, BaseGroup._remove)
    clear = cast(property, BaseGroup._clear)

    def __init__(self, initial_objects: list[TupyObject] = None) -> None:
        if initial_objects is not None:
            for obj in initial_objects:
                self._add(obj)

class Oval(BaseTupyObject):
    def __init__(self, x: int, y: int, width: int, height: int, outline: str = 'black', fill: str = ''):
        self._tkid = window.canvas.create_oval(x, y, x+width, y+height, fill=fill, outline=outline)
        objects.add_object(self)
    
    @property
    def _x(self) -> int:
        return int(window.canvas.coords(self._tkid)[0])
    @_x.setter
    def _x(self, value: int) -> None:
        window.canvas.coords(self._tkid, value, self._y, self._x+self._width, self._y+self._height)
    @property
    def _y(self) -> int:
        return int(window.canvas.coords(self._tkid)[1])
    @_y.setter
    def _y(self, value: int) -> None:
        window.canvas.coords(self._tkid, self._x, value, self._x+self._width, self._y+self._height)
    @property
    def _width(self) -> int:
        return int(window.canvas.coords(self._tkid)[2]) - self._x
    @_width.setter
    def _width(self, value: int) -> None:
        window.canvas.coords(self._tkid, self._x, self._y, self._x+value, self._y+self._height)
    @property
    def _height(self) -> int:
        return int(window.canvas.coords(self._tkid)[3]) - self._y
    @_height.setter
    def _height(self, value: int) -> None:
        window.canvas.coords(self._tkid, self._x, self._y, self._x+self._width, self._y+value)
    @property
    def _fill(self) -> str:
        return str, window.canvas.itemcget(self._tkid, 'fill') # type: ignore
    @_fill.setter
    def _fill(self, value: str) -> None:
        window.canvas.itemconfig(self._tkid, fill=value)
    @property
    def _outline(self) -> str:
        return window.canvas.itemcget(self._tkid, 'outline') # type: ignore
    @_outline.setter
    def _outline(self, value: str) -> None:
        window.canvas.itemconfig(self._tkid, outline=value)

    def destroy(self) -> None:
        window.canvas.delete(self._tkid)

    x = cast(property, _x)
    y = cast(property, _y)
    width = cast(property, _width)
    height = cast(property, _height)
    fill = cast(property, _fill)
    outline = cast(property, _outline)

class Label(BaseTupyObject):
    
    def __init__(self, text: str, x: int, y: int, font: str = 'Arial 20', color: str = 'black', anchor: Literal['nw', 'n', 'ne', 'w', 'center', 'e', 'sw', 's', 'se'] = 'nw') -> None:
        self._tkid = window.canvas.create_text(x, y, text=text, font=font, fill=color, anchor=anchor)
        objects.add_object(self)
    
    @property
    def _x(self) -> int:
        return int(window.canvas.coords(self._tkid)[0])
    @_x.setter
    def _x(self, value: int) -> None:
        window.canvas.coords(self._tkid, value, self._y)
    @property
    def _y(self) -> int:
        return int(window.canvas.coords(self._tkid)[1])
    @_y.setter
    def _y(self, value: int) -> None:
        window.canvas.coords(self._tkid, self._x, value)
    @property
    def text(self) -> str:
        return window.canvas.itemcget(self._tkid, 'text') # type: ignore
    @text.setter
    def text(self, value: str) -> None:
        window.canvas.itemconfig(self._tkid, text=value)
    @property
    def font(self) -> str:
        return window.canvas.itemcget(self._tkid, 'font') # type: ignore
    @font.setter
    def font(self, value: str) -> None:
        window.canvas.itemconfig(self._tkid, font=value)
    @property
    def color(self) -> str:
        return window.canvas.itemcget(self._tkid, 'fill') # type: ignore
    @color.setter
    def color(self, value: str) -> None:
        window.canvas.itemconfig(self._tkid, fill=value)
    @property
    def _width(self) -> int:
        return window.canvas.bbox(self._tkid)[2] - self._x
    @property
    def _height(self) -> int:
        return window.canvas.bbox(self._tkid)[3] - self._y
    @property
    def anchor(self) -> Literal['nw', 'n', 'ne', 'w', 'center', 'e', 'sw', 's', 'se']:
        return window.canvas.itemcget(self._tkid, 'anchor') # type: ignore
    @anchor.setter
    def anchor(self, value: Literal['nw', 'n', 'ne', 'w', 'center', 'e', 'sw', 's', 'se']) -> None:
        window.canvas.itemconfig(self._tkid, anchor=value)

    x = cast(property, _x)
    y = cast(property, _y)

class Rectangle(BaseTupyObject):
    def __init__(self, x: int, y: int, w: int, h: int, outline: str = 'black', fill: str = '') -> None:
        self._tkid = window.canvas.create_rectangle(x, y, x + w, y + h, outline=outline, fill=fill)
        objects.add_object(self)

    @property
    def _x(self) -> int:
        return int(window.canvas.coords(self._tkid)[0])
    @_x.setter
    def _x(self, value: int) -> None:
        window.canvas.coords(self._tkid, value, self._y, value + self._width, self._y + self._height)
    @property
    def _y(self) -> int:
        return int(window.canvas.coords(self._tkid)[1])
    @_y.setter
    def _y(self, value: int) -> None:
        window.canvas.coords(self._tkid, self._x, value, self._x + self._width, value + self._height)
    @property
    def _width(self) -> int:
        return int(window.canvas.coords(self._tkid)[2]) - self._x
    @_width.setter
    def _width(self, value: int) -> None:
        window.canvas.coords(self._tkid, self._x, self._y, self._x + value, self._y + self._height)
    @property
    def _height(self) -> int:
        return int(window.canvas.coords(self._tkid)[3]) - self._y
    @_height.setter
    def _height(self, value: int) -> None:
        window.canvas.coords(self._tkid, self._x, self._y, self._x + self._width, self._y + value)
    @property
    def _fill(self) -> str:
        return window.canvas.itemcget(self._tkid, 'fill') # type: ignore
    @_fill.setter
    def _fill(self, value: str) -> None:
        window.canvas.itemconfig(self._tkid, fill=value)
    @property
    def _outline(self) -> str:
        return window.canvas.itemcget(self._tkid, 'outline') # type: ignore
    @_outline.setter
    def _outline(self, value: str) -> None:
        window.canvas.itemconfig(self._tkid, outline=value)
    
    x = cast(property, _x)
    y = cast(property, _y)
    width = cast(property, _width)
    height = cast(property, _height)
    fill = cast(property, _fill)
    outline = cast(property, _outline)

class PrivateImageAttributes:
    def __init__(self) -> None:
        self.file = ''
        self.angle = 0.0

class BaseImage(BaseTupyObject):
    _attrs: PrivateImageAttributes

    def __new__(cls, *args: Any, **kwargs: Any) -> 'BaseImage':
        self = cast('BaseImage', super().__new__(cls))
        setattr(self, '_attrs', PrivateImageAttributes())
        x = random.randint(0, Window.CANVAS_WIDTH)
        y = random.randint(0, Window.CANVAS_HEIGHT)
        self._initialize(x, y)
        return self

    def __init__(self, file: Optional[str] = None, x: Optional[int] = None, y: Optional[int] = None) -> None:
        super().__init__()
        if file is not None:
            self._file = file
        if x is not None:
            self._x = x
        if y is not None:
            self._y = y

    def _initialize(self, x: int, y: int) -> None:
        # if self._image_path is None:
        self._attrs.file = self.__class__.__name__.lower() + '.png'
        self._image_path = self._find_image_path(self._file)
        self._tkobject = ImageTk.PhotoImage(PILImage.open(self._image_path))
        self._tkid = window.canvas.create_image(x, y, image=self._tkobject)
        objects.add_object(self)

    @property
    def _top_left(self) -> tuple[int, int]:
        return int(self._x - self._width / 2), int(self._y - self._height / 2)

    @property
    def _x(self) -> int:
        return int(window.canvas.coords(self._tkid)[0])
    @_x.setter
    def _x(self, value: int) -> None:
        window.canvas.coords(self._tkid, value, self._y)
    @property
    def _y(self) -> int:
        return int(window.canvas.coords(self._tkid)[1])
    @_y.setter
    def _y(self, value: int) -> None:
        window.canvas.coords(self._tkid, self._x, value)
    @property
    def _width(self) -> int:
        return self._tkobject.width()
    @property
    def _height(self) -> int:
        return self._tkobject.height()
    
    
    @property
    def _angle(self) -> float:
        return self._attrs.angle
    @_angle.setter
    def _angle(self, value: float) -> None:
        self._attrs.angle = value
        self._tkobject = ImageTk.PhotoImage(PILImage.open(self._image_path).rotate(value))
        window.canvas.itemconfig(self._tkid, image=self._tkobject)

    @property
    def _file(self) -> str:
        return self._attrs.file
        
    @_file.setter
    def _file(self, value: str) -> None:
        self._attrs.file = value
        self._image_path = self._find_image_path(value)
        self._tkobject = ImageTk.PhotoImage(PILImage.open(self._image_path))
        window.canvas.itemconfig(self._tkid, image=self._tkobject)
        self._angle = self._angle # Rotate image if needed

    def _find_image_path(self, filename: str) -> str:
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
    x = cast(property, BaseImage._x)
    y = cast(property, BaseImage._y)
    file = cast(property, BaseImage._file)
    angle = cast(property, BaseImage._angle)

    def __new__(cls, *args: Any, **kwargs: Any) -> 'Image':
        self = super().__new__(cls)
        return cast('Image', self)
    

    def __init__(self, file: Optional[str] = None, x: Optional[int] = None, y: Optional[int] = None) -> None:
        super().__init__(file, x, y)

window.create()

def run(globals: dict[str, object]) -> None:
    inspector.env = globals
    window.update_object_pane()
    window.main_loop()
