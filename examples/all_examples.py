import tkinter as tk
import os

examples = [
    'drone-stars.py',
]
examples += sorted([f'pt-br/{f}' for f in os.listdir('../examples/pt-br') if f.endswith('.py')])
keys = [str(i) for i in range(1, 10)] + [chr(i) for i in range(ord('a'), ord('z')+1)]

root = tk.Tk()

def make_callback(example):
    def callback(*args):
        os.system(f'PYTHONPATH=. python ../examples/{example}')
    return callback

tk.Label(text='Examples', font='Arial 18 bold').pack()
for idx, example in enumerate(examples):
    callback = make_callback(example)
    tk.Button(text=f'{keys[idx]} - {example}', command=callback).pack(anchor='w')
    root.bind(f'<Key-{keys[idx]}>', callback)

root.bind(f'<Escape>', lambda _event: root.destroy())
root.mainloop()