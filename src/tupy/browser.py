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

    def configure_ui(self):
        outer = ttk.Frame(self, height=200)
        outer.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.title(_('Objects'))
        self.bind("<Escape>", lambda _event: self.withdraw())
        self.lift()
        
        self.path_label = ttk.Label(outer, text=self.current_path, font=(None, 18, 'bold'))
        self.path_label.pack(side=tk.TOP, fill=tk.X, pady=3)

        self.value_label = ttk.Label(outer, text=self.current_path, font=(None, 16, ''))
        self.value_label.pack(side=tk.TOP, fill=tk.X, pady=3)

        treeview, frame = create_treeview_with_scrollbar(outer)

        treeview.configure(columns=('name'), show='headings')
        treeview.column('name', stretch=tk.YES, width=150)
        treeview.heading('name', text=_('Name'))

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
            self.current_path = f'{self.current_path}.{name}'
            if self.current_path.startswith('.'):
                self.current_path = self.current_path[1:]
            self.update_ui()

    def get_parent(self, name):
        if '.' in name:
            return name[:name.rfind('.')]
        else:
            return ''

    def update_ui(self):
        self.treeview.delete(*self.treeview.get_children())
        if self.current_path == '':
            self.path_label.configure(text=_('Global'))
            self.value_label.configure(text='')
        else:
            self.path_label.configure(text=self.current_path)
            self.value_label.configure(text=repr(self.current_object))
            self.treeview.insert('', tk.END, text='⇦', values=('⇦'))
        for name in self.get_attributes():
            self.treeview.insert('', tk.END, text=name, values=(name))

    @property
    def current_object(self):
        return eval(self.current_path, self.inspector._env)
    
    def get_attributes(self):
        if self.current_path == '':
            return self.inspector.public_variables(type='tupy.TupyObject')
        else:
            return self.inspector.get_public_attributes(self.current_object)