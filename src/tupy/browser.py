import tkinter as tk
import tkinter.ttk as ttk
import tkinter.simpledialog as simpledialog
from tupy.inspector import inspector
from tupy.inspector_model import InspectorModel
from tupy.gui_utils import create_treeview_with_scrollbar

class Browser(ttk.Frame):
    def __init__(self, *args, **kwargs):
        if 'model' in kwargs:
            self.model = kwargs.pop('model')
        else:
            raise ValueError('model is required')
        super().__init__(*args, **kwargs)

        self.model.toplevel_changed.subscribe(lambda x: self.update_ui())

        self.treeview = self.configure_ui()
        self.update_ui()

    def configure_ui(self):
        outer = ttk.Frame(self, height=200)
        outer.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        f = ttk.Frame(outer)
        self.button_back = ttk.Button(f, text='⇦', command=self.model.browse_parent)
        self.button_back.pack(side=tk.LEFT, ipadx=2)

        self.path_label = ttk.Label(f, text=self.model.toplevel_path, font=(None, 18, 'bold'))
        self.path_label.pack(side=tk.LEFT, fill=tk.X, pady=3)
        f.pack(side=tk.TOP, fill=tk.X, pady=3)

        self.value_label = ttk.Label(outer, text=self.model.toplevel_path, font=(None, 16, ''))
        self.value_label.pack(side=tk.TOP, fill=tk.X, pady=3)

        treeview, frame = create_treeview_with_scrollbar(outer)

        treeview.configure(columns=('action', 'name', 'value'), show='headings')
        treeview.column('action', stretch=tk.YES, width=20)
        treeview.column('name', stretch=tk.YES, width=150)
        treeview.column('value', stretch=tk.YES, width=150)
        treeview.heading('action', text='')
        treeview.heading('name', text=_('Name'))
        treeview.heading('value', text=_('Value'))

        treeview.bind('<Button-1>', self._on_item_select)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        return treeview
    
    def _on_item_select(self, event):
        item = self.treeview.identify_row(event.y)
        name = self.treeview.item(item, 'text')
        column = self.treeview.identify_column(event.x)

        COLUMN_ACTION = '#1'
        COLUMN_SELECT = '#2'
        COLUMN_EDIT = '#3'

        if name == self.model.selected_path:
            self.model.selection_changed.notify()
        elif column == COLUMN_ACTION:
            self.model.browse_attribute(item)
        elif column == COLUMN_SELECT:
            self.model.select_attribute(item)
        elif column == COLUMN_EDIT:
            path = self.model.get_full_path(item)
            value = repr(inspector.object_for_variable(path))
            self.will_edit_value(name, value) # TODO: change '' to value

    def will_edit_value(self, attr_name, value):
        new_value_str = simpledialog.askstring(_('Set value'), _('New value for {attr_name}:').format(attr_name=attr_name), initialvalue=value)
        if new_value_str is not None:
            self.notify_edit_listeners(attr_name, new_value_str)
            self.update_ui()

    def update_ui(self):
        self.treeview.delete(*self.treeview.get_children())
        if self.model.toplevel_path == '':
            self.path_label.configure(text=_('Global'))
            self.value_label.configure(text='')
        else:
            value_string = repr(self.model.selected_object)
            value_string = (value_string[:40] + '...') if len(value_string) > 40 else value_string
            self.value_label.configure(text=value_string)
            self.path_label.configure(text=self.model.toplevel_path)
            
            self.treeview.insert('', tk.END, iid='.', text=self.model.toplevel_path, values=('', self.model.toplevel_path, ''))
        for name in self.model.get_attributes():
            iid = name
            if not iid.startswith('['):
                iid = f'.{name}'
            name = f'{self.model.toplevel_path}{iid}'
            if name.startswith('.'):
                name = name[1:]
            value = inspector.object_for_variable(name)
            self.treeview.insert('', tk.END, iid=iid, text=name, values=('⇨', name, repr(value)))
