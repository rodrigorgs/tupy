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
side_panel = tk.Frame(root, bg="light gray")
side_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Add some content to the side panel
def update_side_panel():
    for child in side_panel.winfo_children():
        child.destroy()
    for var in all_variables():
        label = tk.Label(side_panel, text=var)
        label.pack()
# Remove all children from side panel

# label = tk.Label(side_panel, text="Side Panel", font=("Helvetica", 16))
# label.pack(pady=10)

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
        image_path = self.__class__.__name__.lower() + '.png'
        self._img = ImageTk.PhotoImage(Image.open(image_path))
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
    root.mainloop()

# find_closest
# find_overlapping
# scale