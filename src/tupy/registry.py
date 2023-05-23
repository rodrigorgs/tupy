from typing import Iterator, TYPE_CHECKING, Optional
from tupy.tupyobject import TupyObject

# Registry of TupyObjects added to the canvas
class Registry:
    def __init__(self) -> None:
        self._objects: dict[int, TupyObject] = {}
    
    def add_object(self, obj: TupyObject) -> None:
        self._objects[obj._tkid] = obj
    
    def remove_object(self, obj: TupyObject) -> None:
        if '_tkid' in obj.__dict__:
            del self._objects[obj._tkid]
    
    def get_object(self, id: int) -> Optional[TupyObject]:
        return self._objects.get(id, None)

    def __getitem__(self, id: int) -> Optional[TupyObject]:
        return self.get_object(id)

    def __iter__(self) -> Iterator[TupyObject]:
        return iter(self._objects.values())
    def __len__(self) -> int:
        return len(self._objects)
    
    def keys(self) -> list[int]:
        return list(self._objects.keys())