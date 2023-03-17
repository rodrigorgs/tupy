import tkinter as tk
import tkinter.ttk as ttk
import tkinter.simpledialog as simpledialog
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

        treeview.configure(columns=('name', 'value', 'action'), show='headings')
        treeview.column('name', stretch=tk.YES, width=150)
        treeview.column('value', stretch=tk.YES, width=150)
        treeview.column('action', stretch=tk.YES, width=30)
        treeview.heading('name', text=_('Name'))
        treeview.heading('value', text=_('Value'))
        treeview.heading('action', text='')

        treeview.bind('<Button-1>', self._on_item_select)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        return treeview
    
    def _on_item_select(self, event):
        item = self.treeview.identify_row(event.y)
        name = self.treeview.item(item, 'text')
        column = self.treeview.identify_column(event.x)

        COLUMN_ACTION = '#3'
        COLUMN_SELECT = '#1'
        COLUMN_EDIT = '#2'

        if name == '⇦':
            self.current_path = self.get_parent(self.current_path)
            self.update_ui()
            # TODO: remove selection
            self.notify_selection_listeners(self.current_path, self.current_object)
        elif column == COLUMN_ACTION:
            self.current_path = f'{self.current_path}{item}'
            if self.current_path.startswith('.'):
                self.current_path = self.current_path[1:]
            self.update_ui()
            self.notify_selection_listeners(self.current_path, self.current_object)
        elif column == COLUMN_SELECT:
            # TODO: refactor to remove duplication
            path = f'{self.current_path}{item}'
            if path.startswith('.'):
                path = path[1:]
            object = eval(path, self.inspector._env)
            self.notify_selection_listeners(path, object)
        elif column == COLUMN_EDIT:
            # TODO: refactor to remove duplication
            path = f'{self.current_path}{item}'
            if path.startswith('.'):
                path = path[1:]
            value = repr(self.inspector.object_for_variable(path))
            self.will_edit_value(name, value) # TODO: change '' to value

    def will_edit_value(self, attr_name, value):
        new_value_str = simpledialog.askstring(_('Set value'), _('New value for {attr_name}:').format(attr_name=attr_name), initialvalue=value)
        if new_value_str is not None:
            exec(f'{attr_name} = {new_value_str}', self.inspector._env) # TODO: run on console
            self.update_ui()

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
            self.treeview.insert('', tk.END, iid=iid, text=name, values=(name, str(value), '⇨'))

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