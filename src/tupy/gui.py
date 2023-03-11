import random
import traceback
import string
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import tkinter.simpledialog as simpledialog
import tkinter.ttk as ttk
from contextlib import redirect_stdout, redirect_stderr
import io
from tupy.history import CommandHistory
from tupy.browser import Browser

from tupy.gui_utils import create_treeview_with_scrollbar

class Window:
    CANVAS_WIDTH = 640
    CANVAS_HEIGHT = 480
    SIDE_PANE_WIDTH = 280
    UPDATE_DELAY = 1000 // 30

    def __init__(self, inspector, input, common_supertype, registry):
        self._inspector = inspector
        self._common_supertype = common_supertype
        self._input = input
        self._command_history = CommandHistory()
        self._selection_box = None        
        self._selected_object = None
        self._selected_variable = None
        self.is_paused = False
        self.browser = None
        self._registry = registry

    def create(self):
        self.root = tk.Tk()
        self.root.title('Tupy')
        self.root.bind("<Escape>", lambda _event: self.root.destroy())

        # self.create_navigator()

        self.toolbar = self.create_toolbar(self.root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X, pady=3)
        self.twocol = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.twocol.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.tworow = ttk.PanedWindow(self.twocol, orient=tk.VERTICAL)

        self.canvas = self.create_canvas(self.tworow)
        self.canvas.focus_set()

        self._selection_box = self.canvas.create_rectangle(0, 0, 0, 0, outline='')

        self.history_and_console = ttk.Frame(self.tworow)
        self.history_and_console.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.console = self.create_console(self.history_and_console)
        self.history = ScrolledText(self.history_and_console, height=5, font=('Monaco', 14), background='black', foreground='white', wrap=tk.WORD)
        self.history.config(state=tk.DISABLED)
        self.history.tag_config('error', foreground='#ff4136')
        self.history.tag_config('output', foreground='#00BFFF')
        self.history.tag_config('command', foreground='white')
        self.history.tag_config('pale', foreground='darkgray')

        self.history.bind("<1>", lambda event: event.widget.focus_set())
        self.history.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.console.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False)

        self.tworow.add(self.canvas)
        self.tworow.add(self.history_and_console)
        
        self.side_pane = self.create_side_pane(self.twocol)
        
        self.twocol.add(self.tworow)
        self.twocol.add(self.side_pane)
        
    def play(self):
        self.is_paused = False
    def pause(self):
        self.is_paused = True
    def step(self):
        self.is_paused = True
        self.update_objects()

    def create_navigator(self):
        nav = tk.Toplevel(self.root)
        nav.title(_('Objects'))
        nav.bind("<Escape>", lambda _event: nav.withdraw())
        nav.lift()
        nav_tv, nav_tv_frame = create_treeview_with_scrollbar(nav)
        # nav_tv.bind('<<TreeviewSelect>>', self._on_navigator_treeview_select)
        nav_tv_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    def create_toolbar(self, parent):
        toolbar = ttk.Frame(parent, height=30)

        button_run = ttk.Button(toolbar, text="▶", command=self.play)
        button_pause = ttk.Button(toolbar, text="❙❙", command=self.pause)
        button_step = ttk.Button(toolbar, text="▶❙", command=self.step)
        button_add = ttk.Button(toolbar, text="➕ " + _("New object..."), command=self.ask_create_object)
        button_browser = ttk.Button(toolbar, text="ⓘ " + _("Browse objects..."), command=self.browse_objects)

        button_run.pack(side=tk.LEFT, padx=3, ipadx=2, ipady=2)
        button_pause.pack(side=tk.LEFT, padx=3, ipadx=2, ipady=2)
        button_step.pack(side=tk.LEFT, padx=3, ipadx=2, ipady=2)
        button_add.pack(side=tk.RIGHT, padx=3, ipadx=2, ipady=2)
        button_browser.pack(side=tk.RIGHT, padx=3, ipadx=2, ipady=2)

        self.button_pause = button_pause

        toolbar.pack(side=tk.TOP, fill=tk.X, expand=False)
        return toolbar

    def browse_objects(self):
        if self.browser is None:
            self.browser = Browser(self.root, inspector=self._inspector)
            self.browser.bind("<Escape>", lambda _event: self._close_browser())
            self.browser.add_selection_listener(self._on_browser_select)
        else:
            self.browser.lift()
    
    def _close_browser(self):
        self.browser.destroy()
        self.browser = None

    def _on_browser_select(self, path, obj):
        self.select_object(obj, path)
        

    def create_side_pane(self, parent):
        side_pane = ttk.PanedWindow(parent, orient=tk.VERTICAL, width=self.SIDE_PANE_WIDTH)
        side_pane.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        outer_object_pane = self.create_object_pane(side_pane)
        self.object_pane.bind('<<TreeviewSelect>>', lambda event: self.on_click_object(self.object_pane))
        self.member_pane = self.create_member_pane(side_pane)

        side_pane.add(outer_object_pane)
        side_pane.add(self.member_pane)
        
        return side_pane

    def create_object_pane(self, parent):
        outer = ttk.Frame(parent, height=200)
        outer.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        ttk.Label(outer, text=_('Global variables'), font=(None, 18, 'bold')).pack(side=tk.TOP, fill=tk.X, pady=3)
        treeview, frame = create_treeview_with_scrollbar(outer)
        treeview.configure(columns=('name', 'value'), show='headings')
        treeview.column('name', stretch=tk.YES, width=30)
        treeview.column('value', stretch=tk.YES, width=80)
        treeview.heading('name', text=_('Name'))
        treeview.heading('value', text=_('Value (object)'))
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # ttk.Button(outer, text="New object", command=self.ask_create_object).pack(side=tk.BOTTOM, fill=tk.X, pady=3)

        self.object_pane = treeview
        return outer

    def ask_create_object(self):        
        variable = simpledialog.askstring(_("Variable name"), _("Enter a name for the new object\n(must be a valid Python identifier)\nor leave empty for a random name:"))
        if variable is None:
            return
        if variable == '':
            suffix = ''.join(random.choices(string.ascii_lowercase, k=4))
            variable = f'obj_{suffix}'

        classname = simpledialog.askstring(_("Class name"), _("Enter the name of the class to instantiate:"))
        if classname is None:
            return

        # check number of parameters
        klass = self._inspector.object_for_variable(classname)
        method = self._inspector.get_method(klass, '__init__')
        params = self._inspector.method_parameters(method)
        info = self._inspector.method_info(method).replace('(self, ', '(')
        args = ''
        
        if len(params) > 0:
            args = simpledialog.askstring(_("Constructor parameters"), _("Enter the parameters for the constructor of {classname}:\n{info}").format(classname=classname, info=info))

        self._inspector.create_object(variable, classname, args)
        self.update_object_pane()

    def create_member_pane(self, parent):
        member_pane = ttk.Frame(parent)
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
            out = f.getvalue()
            err = g.getvalue()
            ret_suffix = ''
            ret and (" => " + str(ret)) or ""
            self.write_on_history(f'>>> {command.strip()}', tag='command')
            if use_eval and ret is not None:
                self.write_on_history(' => ', tag='pale')
                self.write_on_history(repr(ret), tag='output')
            self.write_on_history(f'\n{out}', tag='output')
            self.write_on_history(f'{err}', tag='error')
            self.update_object_pane()
        except Exception as e:
            self.write_on_history(f'>>> {command}\n', tag='command')
            # tb = traceback.format_exc()
            tb = f'{e.__class__.__name__}: {e}\n'
            self.write_on_history(tb, tag='error')
        finally:
            on_end()
        
        return ret

    def write_on_history(self, text, tag='command'):
        visible = self.history.bbox("end-1c")
        self.history.config(state=tk.NORMAL)
        self.history.insert(tk.END, text, tag)
        if visible is not None:
            self.history.see(tk.END)
        self.history.config(state=tk.DISABLED)

    def submit_console(self, _event):
        self.run_command(self.console.get(), on_end=lambda: self.console.delete(0, tk.END))

    def select_object(self, obj, obj_name):
        self._selected_object = obj
        self._selected_variable = obj_name
        print('select object', obj, obj_name)
        traceback.print_stack(limit=6)
        if obj is None or not self._inspector.object_has_type(obj, self._common_supertype):
            self._selected_object = None
            self._selected_variable = None
            self.canvas.itemconfig(self._selection_box, outline='')
            self.update_member_pane(None, None)
        else:
            self.canvas.itemconfig(self._selection_box, outline='darkgray', dash=(5, 5))
            self.canvas.tag_raise(self._selection_box)
            print('select object', obj)
            self.update_member_pane(obj, obj_name)

    def on_click_object(self, tree):
        index = tree.selection()[0]
        item = tree.item(index)
        obj_name = item['values'][0]
        self._selected_variable = obj_name
        if obj_name == '':
            pass
        elif obj_name is None:
            self.select_object(None, None)
        else:
            self.select_object(self._inspector.object_for_variable(obj_name), obj_name)

    def update_object_pane(self):
        self.object_pane.delete(*self.object_pane.get_children())
        
        for var in [' '] + self._inspector.public_variables(type=self._common_supertype):
            if var == ' ':
                values = ('', '')
            else:
                obj = self._inspector.object_for_variable(var)
                values = (var, str(obj))
            self.object_pane.insert('', 'end', iid=var, text=var, values=values)
        
        if self._selected_variable is not None:
            # if object_pane has key, select it
            if self._selected_variable in self.object_pane.get_children():
                self.object_pane.selection_set(self._selected_variable)
            else:
                print('selection_set \'\'')
                self.object_pane.selection_set(' ')

    def on_click_member(self, tree, obj_name):
        index = tree.selection()[0]
        item = tree.item(index)
        attr_name = item['values'][0]
        value = item['values'][1]
        new_value_str = simpledialog.askstring(_('Set value'), _('New value for {attr_name}:').format(attr_name=attr_name), initialvalue=value)
        if new_value_str is not None:
            new_value = eval(new_value_str)
            setattr(self._selected_object, attr_name, new_value)
            obj = eval(obj_name, self._inspector._env)
            self.update_member_pane(obj, obj_name=obj_name)

    def on_click_method(self, tree, obj_name):
        index = tree.selection()[0]
        item = tree.item(index)
        method_name = item['values'][0]

        print('click method obj_name', obj_name)
        # obj = self._inspector.object_for_variable(obj_name)
        obj = self._selected_object
        print('obj', obj)
        method = self._inspector.get_method(obj, method_name)
        info = self._inspector.method_info(method)
        if self._inspector.method_parameters(method) == []:
            params = ''
        else:
            params = simpledialog.askstring(_("Provide parameters"), _("Comma-separated parameter list:") + "\n" + str(info))
        if params is not None:
            # if obj_name is not None and obj_name != '':
            print('run_command')
            self.run_command(f'{obj_name}.{method_name}({params})', use_eval = True)
            # else:
            #     # params_tuple = self._inspector.eval(f'({params},)')
            #     if params.strip() == '':
            #         ret = method()
            #     else:
            #         params_tuple = (self._inspector.eval(p) for p in params.split(','))
            #         ret = method(*params_tuple)
            #     if ret is not None:
            #         self.write_on_history(f'=> {ret}\n', tag='output')
            self.update_member_pane(obj, obj_name=obj_name)

    def update_member_pane(self, obj, obj_name):
        print('update_member_pane', obj, obj_name)
        traceback.print_stack(limit=6)
        for child in self.member_pane.winfo_children():
            child.destroy()

        if obj is None:
            return
        # if not self._inspector.object_has_type(obj, self._common_supertype):
        #     return
        ttk.Label(self.member_pane, text=_("Object information"), font=(None, 18, 'bold')).pack(side=tk.TOP, fill=tk.X, expand=False)
        ttk.Label(self.member_pane, text=_("Type") + f": {obj.__class__.__name__}, id: 0x{id(obj):02x}", font=(None, 14, 'bold')).pack(side=tk.TOP, fill=tk.X, expand=False)
        ttk.Label(self.member_pane, text=_("Attributes"), font=(None, 14, 'bold')).pack(side=tk.TOP, fill=tk.X, expand=False)

        cols = ('name', 'value', 'class')
        tree, tree_frame = create_treeview_with_scrollbar(self.member_pane)
        tree.configure(columns=cols, show='headings', height=6)
        tree.column('name', stretch=tk.YES, width=50)
        tree.column('value', stretch=tk.YES, width=50)
        tree.column('class', stretch=tk.YES, width=50)
        tree.heading('name', text=_('Name'))
        tree.heading('value', text=_('Value'))
        tree.heading('class', text=_('Value\'s Class'))
        tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

        
        for attr in self._inspector.get_public_attributes(obj):
            attr_value = getattr(obj, attr)
            tuple = (attr, repr(attr_value), type(attr_value).__name__)
            tree.insert('', tk.END, values=tuple)
            tree.bind("<<TreeviewSelect>>", lambda e: self.on_click_member(tree, obj_name))

        ttk.Label(self.member_pane, text=_("Methods"), font=(None, 14, 'bold')).pack(side=tk.TOP, fill=tk.X, expand=False)
        cols = ('name', 'parameters')
        tree_methods, tree_frame_methods = create_treeview_with_scrollbar(self.member_pane)
        tree_methods.configure(columns=cols, show='headings', height=6)
        tree_methods.column('name', stretch=tk.YES, width=50)
        tree_methods.column('parameters', stretch=tk.YES, width=50)
        tree_methods.heading('name', text=_('Name'))
        tree_methods.heading('parameters', text=_('Parameters'))
        tree_frame_methods.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

        for method in self._inspector.get_public_methods(obj):
            if method in ('update', ):
                continue
            params = self._inspector.method_parameters(self._inspector.get_method(obj, method))
            tuple = (method, ', '.join(params))
            tree_methods.insert('', tk.END, values=tuple)
            tree_methods.bind("<<TreeviewSelect>>", lambda e: self.on_click_method(tree_methods, obj_name))

    def update_objects(self):
        updated_object_ids = set()
        for obj in self._inspector.public_objects(type=self._common_supertype):
            if hasattr(obj, 'update') and id(obj) not in updated_object_ids:
                obj.update()
                updated_object_ids.add(id(obj))

    def run_updates(self):
        if not self.is_paused:
            self.update_objects()

        self._input.update()
        if self._selected_object is not None:
            o = self._selected_object
            x, y = o._top_left
            self.canvas.coords(self._selection_box, x, y, x + o._width, y + o._height)
        # TODO: discount update time
        self.root.after(self.UPDATE_DELAY, self.run_updates)

    def select_object_on_canvas(self, event):
        ids = self.canvas.find_closest(event.x, event.y)
        if len(ids) == 1:
            id = ids[0]
            obj = self._registry.get_object(id)
            if (obj is not None) and (not obj._contains_point(event.x, event.y)):
                obj = None
            if obj is None:
                self.select_object(None, None)
            else:
                self.select_object(obj, f"objects[{obj._tkid}]")

    def canvas_click(self, event):
        self._input.on_mouse_press(event)
        if self.canvas.focus_get() is not None:
            self.select_object_on_canvas(event)
        self.canvas.focus_set()

    def main_loop(self):
        self.root.after(self.UPDATE_DELAY, self.run_updates)
        self.canvas.bind('<KeyPress>', self._input.on_key_press)
        self.canvas.bind('<KeyRelease>', self._input.on_key_release)
        self.canvas.bind('<Button-1>', self.canvas_click)
        self.canvas.bind('<ButtonRelease-1>', self._input.on_mouse_release)
        self.canvas.bind('<Motion>', self._input.on_mouse_move)
        self.root.mainloop()
