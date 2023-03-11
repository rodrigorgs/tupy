# Registry of TupyObjects added to the canvas
class Registry:
    def __init__(self) -> None:
        self._objects = {}
    
    def add_object(self, obj):
        self._objects[obj._tkid] = obj
    
    def remove_object(self, obj):
        del self._objects[obj._tkid]
    
    def get_object(self, id):
        print(self._objects)
        return self._objects.get(id, None)