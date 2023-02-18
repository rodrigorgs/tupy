import tkinter as tk
import tkinter.ttk as ttk

class Window:
    def __init__(self, inspector, common_supertype):
        self._inspector = inspector
        self._common_supertype = common_supertype

    def create(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.bind("<Escape>", lambda _event: self.root.destroy())

        self.create_side_pane()
        self.create_canvas()
        self.create_console()

    def create_side_pane(self):
        self.side_pane = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        self.side_pane.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_object_pane()
        self.create_member_pane()

    def create_object_pane(self):
        self.object_pane = tk.Frame(self.side_pane)
        self.side_pane.add(self.object_pane)

    def create_member_pane(self):
        self.member_pane = tk.Frame(self.side_pane)
        self.side_pane.add(self.member_pane)

    def create_canvas(self):
        self.canvas = tk.Canvas(self.root, width=400, height=300, bg="white")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def create_console(self):
        self.console = tk.Entry(self.root, bg="black", fg="white", insertbackground='white')
        self.console.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.console.bind("<Return>", self.submit_console)

    def submit_console(self, _event):
        try:
            exec(self.console.get(), self._inspector._env)
            self.update_object_pane()
        finally:
            self.console.delete(0, tk.END)

    def update_object_pane(self):
        for child in self.object_pane.winfo_children():
            child.destroy()
        for var in self._inspector.public_variables(type=self._common_supertype):
            def make_callback(var):
                def callback(event):
                    self.update_member_pane(var)
                return callback

            label = tk.Label(self.object_pane, text=f'{var}: {type(self._inspector.object_for_variable(var)).__name__}')
            label.bind('<Button-1>', make_callback(var))
            label.pack()

    def update_member_pane(self, obj_name):
        for child in self.member_pane.winfo_children():
            child.destroy()
        obj = self._inspector.object_for_variable(obj_name)
        for member in dir(obj):
            if not member.startswith('_'):
                label = tk.Label(self.member_pane, text=member)
                label.pack()

    def run_updates(self):
        for obj in self._inspector.public_objects(type=self._common_supertype):
            if hasattr(obj, 'update'):
                obj.update()
        self.root.after(50, self.run_updates)

    def main_loop(self):
        self.root.after(50, self.run_updates)
        self.root.mainloop()
