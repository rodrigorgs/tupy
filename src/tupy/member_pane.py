import tkinter as tk
import tkinter.ttk as ttk
import tkinter.simpledialog as simpledialog
from tupy.inspector import inspector
from tupy.inspector_model import InspectorModel
from tupy.gui_utils import create_treeview_with_scrollbar
from typing import Any, Optional, Union
from tupy.translation import _
from tupy.tupyobject import TkEvent

class MemberPane(ttk.Frame):
    def __init__(self, master:Any=None, **kwargs: Any) -> None:
        if 'model' in kwargs:
            self.model = kwargs.pop('model')
        else:
            raise ValueError('model is required')
        if 'run_command' in kwargs:
            self.run_command = kwargs.pop('run_command')
        else:
            raise ValueError('run_command is required')
        super().__init__(master, **kwargs)

        self.model.selection_changed.subscribe(lambda x: self.update_ui())

        # self.treeview = self.configure_ui()
        self.update_ui()

    def update_ui(self) -> None:
        obj = self.model.selected_object
        obj_name = self.model.selected_path

        for child in self.winfo_children():
            child.destroy()

        if obj is None:
            return

        ttk.Label(self, text=_("Object information"), font=(None, 18, 'bold')).pack(side=tk.TOP, fill=tk.X, expand=False)
        ttk.Label(self, text=_("Class") + f": {obj.__class__.__name__}, id: 0x{id(obj):02x}", font=(None, 14, 'bold')).pack(side=tk.TOP, fill=tk.X, expand=False)
        ttk.Label(self, text=_("Attributes"), font=(None, 14, 'bold')).pack(side=tk.TOP, fill=tk.X, expand=False)

        cols = ('name', 'value', 'action')
        tree, tree_frame = create_treeview_with_scrollbar(self)
        tree.configure(columns=cols, show='headings', height=6)
        tree.column('name', stretch=tk.YES, width=50)
        tree.column('value', stretch=tk.YES, width=80)
        tree.column('action', stretch=tk.YES, width=20)
        tree.heading('name', text=_('Name'))
        tree.heading('value', text=_('Value'))
        tree.heading('action', text='')
        tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

        for attr in inspector.get_public_attributes(obj):
            attr_value = getattr(obj, attr)
            tuple = (attr, repr(attr_value), '⇨') #type(attr_value).__name__
            tree.insert('', tk.END, values=tuple)
            tree.bind("<Button-1>", lambda event: self.on_click_attribute(tree, obj_name, event))

        ttk.Label(self, text=_("Methods"), font=(None, 14, 'bold')).pack(side=tk.TOP, fill=tk.X, expand=False)
        cols2 = ('name', 'parameters')
        tree_methods, tree_frame_methods = create_treeview_with_scrollbar(self)
        tree_methods.configure(columns=cols2, show='headings', height=6)
        tree_methods.column('name', stretch=tk.YES, width=50)
        tree_methods.column('parameters', stretch=tk.YES, width=50)
        tree_methods.heading('name', text=_('Name'))
        tree_methods.heading('parameters', text=_('Parameters'))
        tree_frame_methods.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

        for method in inspector.get_public_methods(obj):
            if method in ('update', ):
                continue
            params = inspector.method_parameters(inspector.get_method(obj, method))
            tuple2 = (method, ', '.join(params))
            tree_methods.insert('', tk.END, values=tuple2)
            tree_methods.bind("<<TreeviewSelect>>", lambda e: self.on_click_method(tree_methods, obj_name))


    def on_click_attribute(self, tree: ttk.Treeview, obj_name: str, event: TkEvent) -> None:
        tree.selection_set(tree.identify_row(event.y))
        if len(tree.selection()) == 0:
            return

        column = tree.identify_column(event.x)
        index = tree.selection()[0]
        item = tree.item(index)
        attr_name = item['values'][0]
        value = item['values'][1]

        if column == '#3': # drill down
            self.model.select_absolute_path(self.model.join_paths(obj_name, attr_name))
            # browse_attribute(attr_name)
        else:
            new_value_str = simpledialog.askstring(_('Set value'), _('New value for {attr_name}:').format(attr_name=attr_name), initialvalue=value)
            if new_value_str is not None:
                path = self.model.join_paths(self.model.selected_path, attr_name)
                self.run_command(f'{path} = {new_value_str}')
                self.update_ui()

    def on_click_method(self, tree: ttk.Treeview, obj_name: str) -> None:
        index = tree.selection()[0]
        item = tree.item(index)
        method_name = item['values'][0]

        # obj = inspector.object_for_variable(obj_name)
        obj = self.model.selected_object
        method = inspector.get_method(obj, method_name)
        info = inspector.method_info(method)
        params: Optional[str] = None
        if len(inspector.method_parameters(method)) == 0:
            params = ''
        else:
            params = simpledialog.askstring(_("Provide parameters"), _("Comma-separated parameter list:") + "\n" + str(info))
        if params is not None:
            # if obj_name is not None and obj_name != '':
            self.run_command(f'{obj_name}.{method_name}({params})', use_eval = True)
            # else:
            #     # params_tuple = inspector.eval(f'({params},)')
            #     if params.strip() == '':
            #         ret = method()
            #     else:
            #         params_tuple = (inspector.eval(p) for p in params.split(','))
            #         ret = method(*params_tuple)
            #     if ret is not None:
            #         self.write_on_history(f'=> {ret}\n', tag='output')
            self.update_ui()
