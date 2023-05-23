from typing import Optional

class CommandHistory:
    def __init__(self) -> None:
        self.history: list[str] = []
        self.current = 0
    
    def add(self, command: str) -> None:
        self.history.append(command)
        self.current = len(self.history)
    
    def previous(self) -> Optional[str]:
        if self.current > 0:
            self.current -= 1
            return self.history[self.current]
        else:
            return None
    
    def next(self) -> Optional[str]:
        if self.current < len(self.history):
            self.current += 1
            return self.history[self.current - 1]
        else:
            return None
    
    def clear(self) -> None:
        self.history = []
        self.current = 0
