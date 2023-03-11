# Registry of TupyObjects added to the canvas
class Registry:
    def __init__(self) -> None:
        self._objects = {}
    
    def add_object(self, obj):
        self._objects[obj._tkid] = obj
    
    def remove_object(self, obj):
        if '_tkid' in obj.__dict__:
            del self._objects[obj._tkid]
    
    def get_object(self, id):
        return self._objects.get(id, None)

    def __getitem__(self, id):
        return self.get_object(id)