import tkinter as tk
from PIL import ImageTk, Image

world = []
__global_env = None

def all_variables():
    if __global_env is None:
        return []
    non_private_vars = [x for x in list(__global_env.keys()) if not x.startswith('_')]
    return [x for x in non_private_vars if isinstance(__global_env[x], Objeto)]

# Create the main window
root = tk.Tk()
root.geometry("800x600")

# Create the side panel
side_pane = tk.PanedWindow(root, orient=tk.VERTICAL)
side_pane.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Object pane
# TODO: use a tk.Listbox
object_pane = tk.Frame(side_pane, bg="light gray")
side_pane.add(object_pane)

# Add some content to the side panel
def update_side_panel():
    for child in object_pane.winfo_children():
        child.destroy()
    for var in all_variables():
        def make_callback(var):
            def callback(event):
                update_member_pane(var)
            return callback

        label = tk.Label(object_pane, text=f'{var}: {type(__global_env[var]).__name__}')
        label.bind('<Button-1>', make_callback(var))
        label.pack()
# Member pane
member_pane = tk.Frame(side_pane, bg="light gray")
side_pane.add(member_pane)

# Update member pane
def update_member_pane(obj_name):
    for child in member_pane.winfo_children():
        child.destroy()
    obj = __global_env[obj_name]
    for member in dir(obj):
        if not member.startswith('_'):
            label = tk.Label(member_pane, text=member)
            label.pack()

# Create the canvas
canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create the console
def submit_console(_event):
    try:
        exec(console.get(), __global_env)
        update_side_panel()
    finally:
        console.delete(0, tk.END)

console = tk.Entry(root, bg="black", fg="white", insertbackground='white')
console.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
console.bind("<Return>", submit_console)


##########

class Objeto:
    def __init__(self):
        self._image_path = self.__class__.__name__.lower() + '.png'
        self._img = ImageTk.PhotoImage(Image.open(self._image_path))
        self._sprite = canvas.create_image(50, 50, image=self._img)
        world.append(self)
        print('objeto init')
        print(type(self._sprite))

    @property
    def x(self):
        return canvas.coords(self._sprite)[0]

    @x.setter
    def x(self, value):
        canvas.coords(self._sprite, value, self.y)

    @property
    def y(self):
        return canvas.coords(self._sprite)[1]

    @y.setter
    def y(self, value):
        canvas.coords(self._sprite, self.x, value)

    @property
    def image(self):
        return self._image_path
    @image.setter
    def image(self, value):
        self._image_path = value
        self._img = ImageTk.PhotoImage(Image.open(self._image_path))
        canvas.itemconfig(self._sprite, image=self._img)

    # def __getattr__(self, name):
    #     if not hasattr(self._sprite, name):
    #         raise AttributeError(f"'{name}' not in sprite.")
    #     return lambda: (i for i in getattr(self._sprite, name)())

# Start the main event loop

def run_updates():
    for obj in world:
        if hasattr(obj, 'update'):
            obj.update()
    root.after(50, run_updates)

def run(globals):
    global __global_env
    __global_env = globals
    update_side_panel()
    root.after(50, run_updates)
    root.bind("<Escape>", lambda _event: root.destroy())
    root.mainloop()

# find_closest
# find_overlapping
# scale