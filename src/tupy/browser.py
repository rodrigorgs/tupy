import tkinter as tk
import tkinter.ttk as ttk
import tkinter.simpledialog as simpledialog
from tupy.inspector import inspector
from tupy.inspector_model import InspectorModel
from tupy.gui_utils import create_treeview_with_scrollbar
from typing import Any
from tupy.tupyobject import TkEvent
from tupy.translation import _

class Browser(ttk.Frame):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if 'model' in kwargs:
            self.model = kwargs.pop('model')
        else:
            raise ValueError('model is required')
        super().__init__(*args, **kwargs)

        self.model.toplevel_changed.subscribe(lambda x: self.update_ui())
        self.model.selection_changed.subscribe(lambda x: self.selection_changed())

        self.treeview = self.configure_ui()
        self.update_ui()

    def configure_ui(self) -> ttk.Treeview:
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

        treeview.configure(columns=('action', 'name'), show='headings')
        treeview.column('action', stretch=tk.NO, width=30)
        treeview.column('name', stretch=tk.YES, width=150)
        treeview.heading('action', text='')
        treeview.heading('name', text=_('Name'))

        treeview.bind('<Button-1>', self._on_item_select)
        treeview.bind('<<TreeviewSelect>>', self._tv_select)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        return treeview
    
    def selection_changed(self) -> None:
        # change selection in treeview
        for item in self.treeview.get_children():
            if self.treeview.item(item, 'text') == self.model.selected_subpath:
                self.treeview.selection_set(item)
                break

    def _tv_select(self, _event: Any) -> None:
        if len(self.treeview.selection()) == 0:
            return
        index = self.treeview.selection()[0]
        name = self.treeview.item(index, 'text')
        self.model.select_attribute(name)

    def _on_item_select(self, event: TkEvent) -> None:
        self.treeview.selection_set(self.treeview.identify_row(event.y))
        if len(self.treeview.selection()) == 0:
            return
        item = self.treeview.identify_row(event.y)
        name = self.treeview.item(item, 'text')
        column = self.treeview.identify_column(event.x)

        COLUMN_BROWSE = '#1'
        COLUMN_SELECT = '#2'
        # COLUMN_EDIT = '#3'

        
        if column == COLUMN_BROWSE:
            self.model.browse_attribute(name)
        elif column == COLUMN_SELECT:
            if name == self.model.selected_path:
                self.model.selection_changed.notify()
        # elif column == COLUMN_EDIT:
        #     path = self.model.get_full_path(name)
        #     value = repr(inspector.object_for_variable(path))
        #     self.will_edit_value(name, value) # TODO: change '' to value

    # def will_edit_value(self, attr_name, value):
    #     new_value_str = simpledialog.askstring(_('Set value'), _('New value for {attr_name}:').format(attr_name=attr_name), initialvalue=value)
    #     if new_value_str is not None:
    #         self.notify_edit_listeners(attr_name, new_value_str)
    #         self.update_ui()

    def update_ui(self) -> None:
        self.treeview.delete(*self.treeview.get_children())
        if self.model.toplevel_path == '':
            self.path_label.configure(text=_('Global variables'))
            self.value_label.configure(text='')
        else:
            value_string = repr(self.model.selected_object)
            value_string = (value_string[:40] + '...') if len(value_string) > 40 else value_string
            self.value_label.configure(text=value_string)
            self.path_label.configure(text=self.model.toplevel_path)
            
            self.treeview.insert('', tk.END, iid='.', text='', values=('', 'self'))
        
        for attr_name in self.model.get_attributes(toplevel=True):
            path = self.model.get_full_path(attr_name)
            value = inspector.object_for_variable(path)
            self.treeview.insert('', tk.END, iid=path, text=attr_name, values=('⇨', attr_name))
