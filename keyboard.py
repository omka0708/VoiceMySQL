import tkinter as tk
from tkinter import ttk


class Keyboard(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root, borderwidth=1, relief='groove')

        self.keyboard_isactive = tk.BooleanVar(value=False)
        self.caps_lock = False
        self.root = root
        self.keyboard_isactive.trace_add('write', lambda *args: self.root.on_keyboard())

        for column in range(13):
            self.columnconfigure(index=column, weight=1)
        for row in range(5):
            self.rowconfigure(index=row, weight=1)

        ttk.Button(self, text='~`Ё', command=lambda: self.key_handler('~`Ё')).grid(row=0, column=0)
        ttk.Button(self, text='!1', ).grid(row=0, column=1)
        ttk.Button(self, text='"@', ).grid(row=0, column=2)
        ttk.Button(self, text='№#', ).grid(row=0, column=3)
        ttk.Button(self, text=';$', ).grid(row=0, column=4)
        ttk.Button(self, text='%5', ).grid(row=0, column=5)
        ttk.Button(self, text=':^', ).grid(row=0, column=6)
        ttk.Button(self, text='?&', ).grid(row=0, column=7)
        ttk.Button(self, text='*8', ).grid(row=0, column=8)
        ttk.Button(self, text='(9', ).grid(row=0, column=9)
        ttk.Button(self, text=')0', ).grid(row=0, column=10)
        ttk.Button(self, text='_-', ).grid(row=0, column=11)
        ttk.Button(self, text='+=', ).grid(row=0, column=12)
        ttk.Button(self, text='Backspace', ).grid(row=0, column=13)

        ttk.Label(self, text='OFF', ).grid(row=1, column=0)

        ttk.Button(self, text='Qй', ).grid(row=1, column=1)
        ttk.Button(self, text='Wц', ).grid(row=1, column=2)
        ttk.Button(self, text='Eу', ).grid(row=1, column=3)
        ttk.Button(self, text='Rк', ).grid(row=1, column=4)
        ttk.Button(self, text='Tе', ).grid(row=1, column=5)
        ttk.Button(self, text='Yн', ).grid(row=1, column=6)
        ttk.Button(self, text='Uг', ).grid(row=1, column=7)
        ttk.Button(self, text='Iш', ).grid(row=1, column=8)
        ttk.Button(self, text='Oщ', ).grid(row=1, column=9)
        ttk.Button(self, text='Pз', ).grid(row=1, column=10)
        ttk.Button(self, text='{[х', ).grid(row=1, column=11)
        ttk.Button(self, text='}]ъ', ).grid(row=1, column=12)
        ttk.Button(self, text='|\\/', ).grid(row=1, column=13)

        ttk.Button(self, text='Caps Lock', ).grid(row=2, column=0, columnspan=2)
        ttk.Button(self, text='Aф', ).grid(row=2, column=2)
        ttk.Button(self, text='Sы', ).grid(row=2, column=3)
        ttk.Button(self, text='Dв', ).grid(row=2, column=4)
        ttk.Button(self, text='Fа', ).grid(row=2, column=5)
        ttk.Button(self, text='Gп', ).grid(row=2, column=6)
        ttk.Button(self, text='Hр', ).grid(row=2, column=7)
        ttk.Button(self, text='Jо', ).grid(row=2, column=8)
        ttk.Button(self, text='Kл', ).grid(row=2, column=9)
        ttk.Button(self, text='Lд', ).grid(row=2, column=10)
        ttk.Button(self, text='Ж:;', ).grid(row=2, column=11)
        ttk.Button(self, text='Э"\'', ).grid(row=2, column=12)

        ttk.Button(self, text='Shift', ).grid(row=3, column=0, columnspan=2)
        ttk.Button(self, text='Zя', ).grid(row=3, column=2)
        ttk.Button(self, text='Xч', ).grid(row=3, column=3)
        ttk.Button(self, text='Сc', ).grid(row=3, column=4)
        ttk.Button(self, text='Vм', ).grid(row=3, column=5)
        ttk.Button(self, text='Bи', ).grid(row=3, column=6)
        ttk.Button(self, text='Nт', ).grid(row=3, column=7)
        ttk.Button(self, text='Mь', ).grid(row=3, column=8)
        ttk.Button(self, text='Б<,', ).grid(row=3, column=9)
        ttk.Button(self, text='Ю>.', ).grid(row=3, column=10)
        ttk.Button(self, text='?/', ).grid(row=3, column=11)
        ttk.Button(self, text=',.', ).grid(row=3, column=12)

        ttk.Button(self, text='Space', ).grid(row=4, column=4, columnspan=6, sticky='we')

    def key_handler(self, key_text):
        print(key_text)

    def show_keyboard(self):
        self.grid(row=self.root.grid_size()[1], column=0, columnspan=self.root.grid_size()[0], sticky='we')
        keys = self.grid_slaves()
        keys[len(keys) // 2 - 5].focus_set()
        self.update()

    def hide_keyboard(self):
        self.grid_remove()
        self.root.focused_entry.focus_set()
