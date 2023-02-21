import random
import string
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import tkinter.simpledialog as simpledialog
import tkinter.ttk as ttk
from contextlib import redirect_stdout, redirect_stderr
import io
import traceback
from tupy.history import CommandHistory

class Window:
    CANVAS_WIDTH = 640
    CANVAS_HEIGHT = 480
    SIDE_PANE_WIDTH = 280
    UPDATE_DELAY = 1000 // 30

    def __init__(self, inspector, input, common_supertype):
        self._inspector = inspector
        self._common_supertype = common_supertype
        self._input = input
        self._command_history = CommandHistory()

    def create(self):
        self.root = tk.Tk()
        # self.root.geometry("800x600")
        self.root.bind("<Escape>", lambda _event: self.root.destroy())

        self.twocol = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.twocol.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.tworow = ttk.PanedWindow(self.twocol, orient=tk.VERTICAL)

        self.canvas = self.create_canvas(self.tworow)
        self.canvas.focus_set()

        # self.console = self.create_console(self.tworow)

        self.history_and_console = ttk.Frame(self.tworow)
        self.history_and_console.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.console = self.create_console(self.history_and_console)
        self.history = ScrolledText(self.history_and_console, height=5, font=('Monaco', 14), background='black', foreground='white', wrap=tk.WORD)
        self.history.config(state=tk.DISABLED)
        self.history.bind("<1>", lambda event: event.widget.focus_set())
        self.history.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.console.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False)

        self.tworow.add(self.canvas)
        self.tworow.add(self.history_and_console)
        
        self.side_pane = self.create_side_pane(self.twocol)
        
        self.twocol.add(self.tworow)
        self.twocol.add(self.side_pane)
        

    def create_side_pane(self, parent):
        side_pane = ttk.PanedWindow(parent, orient=tk.VERTICAL, width=self.SIDE_PANE_WIDTH)
        side_pane.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        outer_object_pane = self.create_object_pane(side_pane)
        self.member_pane = self.create_member_pane(side_pane)

        side_pane.add(outer_object_pane)
        side_pane.add(self.member_pane)
        
        return side_pane

    def create_object_pane(self, parent):
        outer = ttk.Frame(parent, height=200)

        ttk.Label(outer, text="Objects", font=(None, 18, 'bold')).pack(side=tk.TOP, fill=tk.X, pady=3)
        ttk.Button(outer, text="New object", command=self.ask_create_object).pack(side=tk.BOTTOM, fill=tk.X, pady=3)

        canvas = tk.Canvas(outer)
        scrollbar = ttk.Scrollbar(outer, orient=tk.VERTICAL, command=canvas.yview)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        frame = ttk.Frame(canvas)
        frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")

        self.object_pane = frame


        return outer

    # TODO: currently does not support parameters in the constructor
    def ask_create_object(self):        
        classname = simpledialog.askstring("Class name", f"Enter the name of the class to instantiate:")
        if classname is None:
            return

        variable = simpledialog.askstring("Variable name", f"Enter a name for the new object (must be a valid Python identifier) or leave empty for a random name:")
        if variable is None or variable == '':
            suffix = ''.join(random.choices(string.ascii_lowercase, k=4))
            variable = f'obj_{suffix}'

        self._inspector.create_object(variable, classname)
        self.update_object_pane()

    def create_member_pane(self, parent):
        member_pane = ttk.Frame(parent)
        # self.side_pane.add(self.member_pane)
        return member_pane

    def create_canvas(self, parent):
        canvas = tk.Canvas(parent, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT, bg="white")
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.bind("<1>", lambda event: event.widget.focus_set())
        return canvas

    def create_console(self, parent):
        style = ttk.Style()
        style.configure('console.TEntry', foreground='white', background='black', insertcolor='white')

        console = ttk.Entry(parent, style='console.TEntry', font=('Monaco', 16))
        console.bind("<Return>", self.submit_console)
        console.bind("<Up>", self.history_up)
        console.bind("<Down>", self.history_down)
        return console

    def history_up(self, event):
        command = self._command_history.previous()
        self.console.delete(0, tk.END)
        if command is not None:
            self.console.insert(0, command)

    def history_down(self, event):
        command = self._command_history.next()
        self.console.delete(0, tk.END)
        if command is not None:
            self.console.insert(0, command)

    def run_command(self, command, on_end=lambda: None, use_eval=False):
        self._command_history.add(command)
        ret = None
        try:
            f = io.StringIO()
            g = io.StringIO()
            with redirect_stdout(f):
                with redirect_stderr(g):
                    if use_eval:
                        ret = eval(command, self._inspector._env)
                    else:
                        exec(command, self._inspector._env)
            s1 = f.getvalue()
            s2 = g.getvalue()
            ret_suffix = ''
            if use_eval and ret is not None:
                ret_suffix = ' => ' + repr(ret)
            ret and (" => " + str(ret)) or ""
            self.write_on_history(f'>>> {command}{ret_suffix}\n')
            self.write_on_history(f'{s1}{s2}')
            self.update_object_pane()
        except Exception as e:
            self.write_on_history(f'>>> {command}\n')
            # tb = traceback.format_exc()
            tb = f'{e.__class__.__name__}: {e}\n'
            self.write_on_history(tb)
        finally:
            on_end()
        
        return ret

    def write_on_history(self, text):
        visible = self.history.bbox("end-1c")
        self.history.config(state=tk.NORMAL)
        self.history.insert(tk.END, text)
        if visible is not None:
            self.history.see(tk.END)
        self.history.config(state=tk.DISABLED)

    def submit_console(self, _event):
        self.run_command(self.console.get(), on_end=lambda: self.console.delete(0, tk.END))

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
                obj = self._inspector.object_for_variable(obj_name)
                method = self._inspector.get_method(obj, member_name)
                info = self._inspector.method_info(method)
                if self._inspector.method_parameters(method) == []:
                    params = ''
                else:
                    params = simpledialog.askstring("Provide parameters", f"Comma-separated parameter list:\n{info}")
                if params is not None:
                    self.run_command(f'{obj_name}.{member_name}({params})', use_eval = True)
                    self.update_member_pane(obj_name)
            return callback

        for child in self.member_pane.winfo_children():
            child.destroy()

        ttk.Label(self.member_pane, text=f'{obj_name}', font=(None, 18, 'bold')).pack(side=tk.TOP, fill=tk.X, expand=False)

        cols = ('name', 'value', 'type')
        tree = ttk.Treeview(self.member_pane, columns=cols, show='headings', height=6)
        tree.column('name', stretch=tk.YES, width=50)
        tree.column('value', stretch=tk.YES, width=50)
        tree.column('type', stretch=tk.YES, width=50)
        tree.heading('name', text='Name')
        tree.heading('value', text='Value')
        tree.heading('type', text='Type')
        tree.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

        if obj_name in self._inspector.public_variables(type=self._common_supertype):
            obj = self._inspector.object_for_variable(obj_name)
            
            for attr in self._inspector.get_public_attributes(obj):
                tuple = (attr, repr(getattr(obj, attr)), type(getattr(obj, attr)).__name__)
                tree.insert('', tk.END, values=tuple)

            for method in self._inspector.get_public_methods(obj):
                if method in ('update', ):
                    continue
                params = self._inspector.method_parameters(self._inspector.get_method(obj, method))
                button = ttk.Button(self.member_pane, text=f'{method}({", ".join(params)})',
                                    command=make_callback(obj_name, method))
                button.pack(anchor=tk.W, padx=5)

    def run_updates(self):
        for obj in self._inspector.public_objects(type=self._common_supertype):
            if hasattr(obj, 'update'):
                obj.update()
        self._input.update()
        # TODO: discount update time
        self.root.after(self.UPDATE_DELAY, self.run_updates)

    def main_loop(self):
        self.root.after(self.UPDATE_DELAY, self.run_updates)
        self.canvas.bind("<KeyPress>", self._input.on_key_press)
        self.canvas.bind("<KeyRelease>", self._input.on_key_release)
        self.root.mainloop()
