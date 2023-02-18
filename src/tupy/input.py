# TODO: mouse input
class InputMap:
    def __init__(self) -> None:
        # keymap:
        # = 0: button up
        # = 2: button just down
        # = 1: button down (but not just down)
        # > 0 and < 1: just up (used for debouncing)
        self.keymap: dict = {}
    
    def on_key_press(self, event):
        # print('keypress', event.keysym, self.keymap.get(event.keysym, 0))
        if self.keymap.get(event.keysym, 0) == 0:
            self.keymap[event.keysym] = 2
        else:
            self.keymap[event.keysym] = 1
    
    def on_key_release(self, event):
        # print('key release', event.keysym)
        self.keymap[event.keysym] = 0.5
    
    def update(self):
        # print(self.keymap)
        for key in self.keymap:
            # just pressed => pressed
            if self.keymap.get(key, 0) == 2:
                self.keymap[key] = 1
            # just released, decrement for debouncing
            elif self.keymap.get(key, 0) > 0:
                self.keymap[key] -= 0.25

    def is_key_down(self, key):
        return self.keymap.get(key, 0) > 0
    
    def is_key_just_down(self, key):
        return self.keymap.get(key, 0) == 2
    
    def is_key_up(self, key):
        return self.keymap.get(key, 0) == 0