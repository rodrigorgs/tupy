from typing import Protocol, runtime_checkable

@runtime_checkable
class TkEvent(Protocol):
    x: int
    y: int
    keysym: str

@runtime_checkable
class TupyObject(Protocol):
    _x: int
    _y: int
    # _width: int
    # _height: int
    _tkid: int

    def update(self) -> None:
        pass

    def _destroy(self) -> None:
        pass

    def _hide(self) -> None:
        pass
    def _show(self) -> None:
        pass

    def _position(self) -> tuple[int, int]:
        return (0, 0)

    def _contains_point(self, px: int, py: int) -> bool:
        return False

    def _collides_with(self, other: 'TupyObject') -> bool:
        return False

    @property
    def _top_left(self) -> tuple[int, int]:
        return (0, 0)
    
    @property
    def _width(self) -> int:
        return 0

    @property
    def _height(self) -> int:
        return 0
    