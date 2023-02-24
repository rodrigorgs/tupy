import tkinter as tk
import os

examples = '''
drone-stars.py
'''.strip().split('\n')

root = tk.Tk()

def make_callback(example):
    def callback(*args):
        os.system(f'PYTHONPATH=. python ../examples/{example}')
    return callback

tk.Label(text='Examples', font='Arial 18 bold').pack()
for idx, example in enumerate(examples):
    callback = make_callback(example)
    tk.Button(text=example, command=callback).pack()
    root.bind(f'<Key-{idx+1}>', callback)

root.bind(f'<Escape>', lambda _event: root.destroy())
root.mainloop()