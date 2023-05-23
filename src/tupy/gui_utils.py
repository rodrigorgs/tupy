import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Misc
from typing import Optional

def create_treeview_with_scrollbar(parent: Optional[Misc]) -> tuple[ttk.Treeview, ttk.Frame]:
    frame = ttk.Frame(parent, height=150)
    treeview = ttk.Treeview(frame)
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=treeview.yview)
    treeview.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    return (treeview, frame)
