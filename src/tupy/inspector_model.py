from tupy.inspector import inspector
from tupy.registry import Registry
from typing import Callable, Any, Optional
from tupy. tupyobject import TupyObject

class Event:
    def __init__(self, name: str, data: object = None) -> None:
        self.name = name
        self.data = data
        self.callbacks: list[Callable[[Any], Any]] = []
    
    def subscribe(self, callback: Callable[[Any], Any]) -> None:
        self.callbacks.append(callback)
    
    def unsubscribe(self, callback: Callable[[Any], Any]) -> None:
        self.callbacks.remove(callback)
    
    def notify(self, data: Any = None) -> None:
        for callback in self.callbacks:
            callback(data or self.data)

class InspectorModel:
    def __init__(self) -> None:
        self.toplevel_path = ''
        self.selected_subpath = ''
        
        self.toplevel_changed = Event('toplevel_changed')
        self.selection_changed = Event('selected_path_changed')
        # self.edit_attribute = Event('edit_attribute')
        # self.call_method = Event('call_method')

    def browse_parent(self) -> None:
        self.toplevel_path = self.get_parent(self.toplevel_path)
        self.selected_subpath = ''
        self.toplevel_changed.notify()
        self.selection_changed.notify()

    def browse_attribute(self, attr_name: str) -> None:
        self.toplevel_path = self.join_paths(self.toplevel_path, attr_name)
        self.selected_subpath = ''
        self.toplevel_changed.notify()
        self.selection_changed.notify()
    
    def select_absolute_path(self, path: str) -> None:
        if path is None or path == '':
            self.toplevel_path = ''
            self.selected_subpath = ''
            self.toplevel_changed.notify()
            self.selection_changed.notify()
        else:
            obj = inspector.eval(path)
            # Look for object in current toplevel
            for attr in self.get_attributes(toplevel=True):
                if inspector.object_for_variable(self.get_full_path(attr)) is obj:
                    self.select_attribute(attr)
                    return
            # If not found, change toplevel
            self.toplevel_path = self.get_parent(path)
            self.selected_subpath = path[len(self.toplevel_path):]
            if self.selected_subpath.startswith('.'):
                self.selected_subpath = self.selected_subpath[1:]
            # print('select absolute path', self.toplevel_path, self.selected_subpath)
            self.toplevel_changed.notify()
            self.selection_changed.notify()

    def select_attribute(self, attr_name: str) -> None:
        if self.selected_subpath != attr_name:
            self.selected_subpath = attr_name
            self.selection_changed.notify()

    def get_full_path(self, path: str) -> str:
        return self.join_paths(self.toplevel_path, path)

    @staticmethod
    def get_parent(path: str) -> str:
        last_index = max(path.rfind('['), path.rfind('.'))
        if last_index > -1:
            return path[:last_index]
        else:
            return ''

    @staticmethod
    def join_paths(parent: str, child: str) -> str:
        if not (child == '' or child.startswith('[') or child.startswith('.')):
            child = '.' + child
        path = f'{parent}{child}'
        if path.startswith('.'):
            path = path[1:]
        return path

    @property
    def selected_path(self) -> str:
        return self.get_full_path(self.selected_subpath)

    def get_attributes(self, toplevel: bool = False) -> list[str]:
        path = self.selected_path if not toplevel else self.toplevel_path
        if path == '':
            return inspector.public_variables(type=TupyObject)
        else:
            obj = inspector.eval(path) #self.selected_object
            if isinstance(obj, dict) or isinstance(obj, Registry):
                return [f'[{repr(k)}]' for k in obj.keys()]
            elif hasattr(obj, '__len__') and hasattr(obj, '__getitem__'):
                return [f'[{i}]' for i in range(len(obj))]
            else:
                return inspector.get_public_attributes(obj)

    def get_methods(self) -> list[str]:
        if self.selected_path == '':
            return []
        else:
            methods = inspector.get_public_methods(self.selected_object)
            return [m for m in methods if m not in ('update', )]
        
    @property
    def selected_object(self) -> Any:
        if self.selected_path == '':
            return None
        return inspector.eval(self.selected_path)
