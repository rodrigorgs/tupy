import tkinter as tk
import tkinter.ttk as ttk
from tupy.gui_utils import create_treeview_with_scrollbar

class Browser(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        if 'inspector' in kwargs:
            self.inspector = kwargs['inspector']
            del kwargs['inspector']
        super().__init__(*args, **kwargs)

        self.current_path = ''

        self.treeview = self.configure_ui()
        self.update_ui()
        self.selection_listeners = []

    def add_selection_listener(self, listener):
        self.selection_listeners.append(listener)
    def remove_selection_listener(self, listener):
        self.selection_listeners.remove(listener)
    def notify_selection_listeners(self, path, object):
        for listener in self.selection_listeners:
            listener(path, object)

    def configure_ui(self):
        outer = ttk.Frame(self, height=200)
        outer.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.title(_('Objects'))
        self.lift()
        
        self.path_label = ttk.Label(outer, text=self.current_path, font=(None, 18, 'bold'))
        self.path_label.pack(side=tk.TOP, fill=tk.X, pady=3)

        self.value_label = ttk.Label(outer, text=self.current_path, font=(None, 16, ''))
        self.value_label.pack(side=tk.TOP, fill=tk.X, pady=3)

        treeview, frame = create_treeview_with_scrollbar(outer)

        treeview.configure(columns=('name', 'value'), show='headings')
        treeview.column('name', stretch=tk.YES, width=150)
        treeview.column('value', stretch=tk.YES, width=150)
        treeview.heading('name', text=_('Name'))
        treeview.heading('value', text=_('Value'))

        treeview.bind('<<TreeviewSelect>>', self._on_item_select)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        return treeview
    
    def _on_item_select(self, event):
        item = self.treeview.selection()[0]
        name = self.treeview.item(item, 'text')

        if name == '⇦':
            self.current_path = self.get_parent(self.current_path)
            self.update_ui()
        else:
            self.current_path = f'{self.current_path}{item}'
            if self.current_path.startswith('.'):
                self.current_path = self.current_path[1:]
            self.update_ui()
        
        self.notify_selection_listeners(self.current_path, self.current_object)

    def get_parent(self, name):
        if '.' in name:
            last_index = max(name.rfind('['), name.rfind('.'))
            return name[:last_index]
        else:
            return ''

    def update_ui(self):
        self.treeview.delete(*self.treeview.get_children())
        if self.current_path == '':
            self.path_label.configure(text=_('Global'))
            self.value_label.configure(text='')
        else:
            value_string = repr(self.current_object)
            value_string = (value_string[:40] + '...') if len(value_string) > 40 else value_string
            self.value_label.configure(text=value_string)
            self.path_label.configure(text=self.current_path)
            
            self.treeview.insert('', tk.END, iid='⇦', text='⇦', values=('⇦'))
        for name in self.get_attributes():
            iid = name
            if not iid.startswith('['):
                iid = f'.{name}'
            name = f'{self.current_path}{iid}'
            if name.startswith('.'):
                name = name[1:]
            value = self.inspector.object_for_variable(name)
            self.treeview.insert('', tk.END, iid=iid, text=name, values=(name, str(value)))

    @property
    def current_object(self):
        return eval(self.current_path, self.inspector._env)
    
    def get_attributes(self):
        if self.current_path == '':
            return self.inspector.public_variables(type='tupy.TupyObject')
        else:
            obj = self.current_object
            if isinstance(obj, (list, tuple)):
                return [f'[{i}]' for i in range(len(obj))]
            elif isinstance(obj, dict):
                return [f'[{repr(k)}]' for k in obj.keys()]
            else:
                return self.inspector.get_public_attributes(self.current_object)