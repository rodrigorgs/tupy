class CommandHistory:
    def __init__(self):
        self.history = []
        self.current = 0
    
    def add(self, command):
        self.history.append(command)
        self.current = len(self.history)
    
    def previous(self):
        if self.current > 0:
            self.current -= 1
            return self.history[self.current]
        else:
            return None
    
    def next(self):
        if self.current < len(self.history):
            self.current += 1
            return self.history[self.current - 1]
        else:
            return None
    
    def clear(self):
        self.history = []
        self.current = 0
