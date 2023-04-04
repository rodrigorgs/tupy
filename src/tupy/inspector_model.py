from tupy.inspector import inspector

class Event:
    def __init__(self, name: str, data: object = None) -> None:
        self.name = name
        self.data = data
        self.callbacks = []
    
    def subscribe(self, callback):
        self.callbacks.append(callback)
    
    def unsubscribe(self, callback):
        self.callbacks.remove(callback)
    
    def notify(self, data=None):
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

    def browse_parent(self):
        self.toplevel_path = self.get_parent(self.toplevel_path)
        self.selected_subpath = ''
        self.toplevel_changed.notify()
        self.selection_changed.notify()

    def browse_attribute(self, attr_name):
        self.toplevel_path = self.join_paths(self.toplevel_path, attr_name)
        self.selected_subpath = ''
        self.toplevel_changed.notify()
        self.selection_changed.notify()
    
    def select_attribute(self, attr_name):
        self.selected_subpath = attr_name
        self.selection_changed.notify()

    def get_full_path(self, path):
        return self.join_paths(self.toplevel_path, path)

    @staticmethod
    def get_parent(path):
        if '.' in path:
            last_index = max(path.rfind('['), path.rfind('.'))
            return path[:last_index]
        else:
            return ''

    @staticmethod
    def join_paths(parent, child):
        path = f'{parent}{child}'
        if path.startswith('.'):
            path = path[1:]
        return path

    @property
    def selected_path(self):
        return self.get_full_path(self.selected_subpath)

    def get_attributes(self) -> list[str]:
        if self.selected_path == '':
            return inspector.public_variables(type='tupy.TupyObject')
        else:
            obj = self.selected_object
            if isinstance(obj, (list, tuple)):
                return [f'[{i}]' for i in range(len(obj))]
            elif isinstance(obj, dict):
                return [f'[{repr(k)}]' for k in obj.keys()]
            else:
                return inspector.get_public_attributes(self.selected_object)

    def get_methods(self) -> list[str]:
        if self.selected_path == '':
            return []
        else:
            methods = inspector.get_public_methods(self.selected_object)
            return [m for m in methods if m not in ('update', )]
        
    @property
    def selected_object(self):
        if self.selected_path == '':
            return None
        return inspector.eval(self.selected_path)
