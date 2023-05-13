# TODO: mouse input

class MouseMap:
    def __init__(self) -> None:
        # 2 = just pressed
        # 1 = pressed
        # 0 = released
        self.mouse_button = 0
        self.mouse_location = (0, 0)

    def update(self):
        if self.mouse_button == 2:
            self.mouse_button = 1

    def on_mouse_press(self, event):
        self.mouse_button = 2
    def on_mouse_release(self, event):
        self.mouse_button = 0
    def on_mouse_move(self, event):
        self.mouse_location = (event.x, event.y)

    def is_button_down(self):
        return self.mouse_button >= 1
    def is_button_just_down(self):
        return self.mouse_button == 2
    @property
    def x(self):
        return self.mouse_location[0]
    @property
    def y(self):
        return self.mouse_location[1]

class KeyboardMap:
    def __init__(self) -> None:
        # keymap:
        # = 0: button up
        # = 2: button just down
        # = 1: button down (but not just down)
        # > 0 and < 1: just up (used for debouncing)
        self.keymap: dict = {}

    def on_key_press(self, event):
        # print(event.keysym)
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