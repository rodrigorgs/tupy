import tkinter as tk
import tkinter.ttk as ttk

def create_treeview_with_scrollbar(parent):
    frame = ttk.Frame(parent)
    treeview = ttk.Treeview(frame)
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=treeview.yview)
    treeview.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    return (treeview, frame)
