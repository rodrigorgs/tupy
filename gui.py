import tkinter as tk
import tkinter.ttk as ttk
from input import InputMap

class Window:
    def __init__(self, inspector, input, common_supertype):
        self._inspector = inspector
        self._common_supertype = common_supertype
        self._input = input

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
        outer = ttk.Frame(self.side_pane, height=200)
        self.side_pane.add(outer)

        canvas = tk.Canvas(outer)
        scrollbar = ttk.Scrollbar(outer, orient=tk.VERTICAL, command=canvas.yview)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        frame = ttk.Frame(canvas)
        frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")

        self.object_pane = frame

    def create_member_pane(self):
        self.member_pane = ttk.Frame(self.side_pane)
        self.side_pane.add(self.member_pane)

    def create_canvas(self):
        self.canvas = tk.Canvas(self.root, width=400, height=300, bg="white")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.bind("<1>", lambda event: event.widget.focus_set())

    def create_console(self):
        self.console = ttk.Entry(self.root) #, bg="black", fg="white", insertbackground='white')
        self.console.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.console.bind("<Return>", self.submit_console)

    def run_command(self, command):
        try:
            exec(command, self._inspector._env)
            self.update_object_pane()
        finally:
            pass

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

            label = ttk.Label(self.object_pane, text=f'{var}: {type(self._inspector.object_for_variable(var)).__name__}')
            label.bind('<Button-1>', make_callback(var))
            label.pack(padx=5, anchor=tk.W)

    def update_member_pane(self, obj_name):
        def make_callback(obj_name, member_name):
            def callback():
                self.run_command(f'{obj_name}.{member_name}()')
                self.update_member_pane(obj_name)
            return callback

        for child in self.member_pane.winfo_children():
            child.destroy()

        if obj_name in self._inspector.public_variables(type=self._common_supertype):
            obj = self._inspector.object_for_variable(obj_name)
            for attr in self._inspector.get_public_attributes(obj):
                label = tk.Label(self.member_pane, text=f'{attr}: {getattr(obj, attr)}')
                label.pack(anchor=tk.W, padx=5)
            for method in self._inspector.get_public_methods(obj):
                button = ttk.Button(self.member_pane, text=f'{method}()',
                                    command=make_callback(obj_name, method))
                button.pack(anchor=tk.W, padx=5)

    def run_updates(self):
        for obj in self._inspector.public_objects(type=self._common_supertype):
            if hasattr(obj, 'update'):
                obj.update()
        self._input.update()
        self.root.after(50, self.run_updates)

    def main_loop(self):
        self.root.after(50, self.run_updates)
        self.canvas.bind("<KeyPress>", self._input.on_key_press)
        self.canvas.bind("<KeyRelease>", self._input.on_key_release)
        self.root.mainloop()
