import tkinter as tk
from tkinter import ttk
import settings as st


class Keyboard(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root, borderwidth=1, relief='groove')

        self.keyboard_isactive = tk.BooleanVar(value=False)
        self.capslock = False
        self.shift = False
        self.root = root
        self.tkvars = {
            'capslock': tk.StringVar(value='Caps Lock (OFF)'),
            'shift': tk.StringVar(value='Shift (OFF)')}
        self.keyboard_isactive.trace_add('write', lambda *args: self.root.on_keyboard())

        for column in range(13):
            self.columnconfigure(index=column, weight=1)
        for row in range(5):
            self.rowconfigure(index=row, weight=1)

        ttk.Button(self, text='~`Ё', command=lambda: self.key_handler('~~``ёЁЁё')).grid(row=0, column=0)
        ttk.Button(self, text='!1', command=lambda: self.key_handler('!!11!!11')).grid(row=0, column=1)
        ttk.Button(self, text='"@', command=lambda: self.key_handler('@@22""22')).grid(row=0, column=2)
        ttk.Button(self, text='№#', command=lambda: self.key_handler('##33№№33')).grid(row=0, column=3)
        ttk.Button(self, text=';$', command=lambda: self.key_handler('$$44;;44')).grid(row=0, column=4)
        ttk.Button(self, text='%5', command=lambda: self.key_handler('%%55%%55')).grid(row=0, column=5)
        ttk.Button(self, text=':^', command=lambda: self.key_handler('^^66::66')).grid(row=0, column=6)
        ttk.Button(self, text='?&', command=lambda: self.key_handler('&&77??77')).grid(row=0, column=7)
        ttk.Button(self, text='*8', command=lambda: self.key_handler('**88**88')).grid(row=0, column=8)
        ttk.Button(self, text='(9', command=lambda: self.key_handler('((99((99')).grid(row=0, column=9)
        ttk.Button(self, text=')0', command=lambda: self.key_handler('))00))00')).grid(row=0, column=10)
        ttk.Button(self, text='_-', command=lambda: self.key_handler('__--__--')).grid(row=0, column=11)
        ttk.Button(self, text='+=', command=lambda: self.key_handler('++==++==')).grid(row=0, column=12)
        ttk.Button(self, text='Backspace', command=lambda: self.key_handler('backspace')).grid(row=0, column=13)

        # root.root = main App
        ttk.Button(self, textvariable=self.root.root.tkvars['language'], text=st.LANGUAGE,
                   command=lambda: self.key_handler('language')).grid(row=1, column=0)

        ttk.Button(self, text='Qй', command=lambda: self.key_handler('qQQqйЙЙй')).grid(row=1, column=1)
        ttk.Button(self, text='Wц', command=lambda: self.key_handler('wWWwцЦЦц')).grid(row=1, column=2)
        ttk.Button(self, text='Eу', command=lambda: self.key_handler('eEEeуУУу')).grid(row=1, column=3)
        ttk.Button(self, text='Rк', command=lambda: self.key_handler('rRRrкККк')).grid(row=1, column=4)
        ttk.Button(self, text='Tе', command=lambda: self.key_handler('tTTtеЕЕе')).grid(row=1, column=5)
        ttk.Button(self, text='Yн', command=lambda: self.key_handler('yYYyнННн')).grid(row=1, column=6)
        ttk.Button(self, text='Uг', command=lambda: self.key_handler('uUUuгГГг')).grid(row=1, column=7)
        ttk.Button(self, text='Iш', command=lambda: self.key_handler('iIIiшШШш')).grid(row=1, column=8)
        ttk.Button(self, text='Oщ', command=lambda: self.key_handler('oOOoщЩЩщ')).grid(row=1, column=9)
        ttk.Button(self, text='Pз', command=lambda: self.key_handler('pPPpзЗЗз')).grid(row=1, column=10)
        ttk.Button(self, text='{[х', command=lambda: self.key_handler('{{[[хХХх')).grid(row=1, column=11)
        ttk.Button(self, text='}]ъ', command=lambda: self.key_handler('}}]]ъЪЪъ')).grid(row=1, column=12)
        ttk.Button(self, text='|\\/', command=lambda: self.key_handler('||\\\\//\\\\')).grid(row=1, column=13)

        ttk.Button(self, textvariable=self.tkvars['capslock'],
                   command=lambda: self.key_handler('capslock')).grid(row=2, column=0, columnspan=3, sticky='we')
        ttk.Button(self, text='Aф', command=lambda: self.key_handler('aAAaфФФф')).grid(row=2, column=3)
        ttk.Button(self, text='Sы', command=lambda: self.key_handler('sSSsыЫЫы')).grid(row=2, column=4)
        ttk.Button(self, text='Dв', command=lambda: self.key_handler('dDDdвВВв')).grid(row=2, column=5)
        ttk.Button(self, text='Fа', command=lambda: self.key_handler('fFFfаААа')).grid(row=2, column=6)
        ttk.Button(self, text='Gп', command=lambda: self.key_handler('gGGgпППп')).grid(row=2, column=7)
        ttk.Button(self, text='Hр', command=lambda: self.key_handler('hHHhрРРр')).grid(row=2, column=8)
        ttk.Button(self, text='Jо', command=lambda: self.key_handler('jJJjоООо')).grid(row=2, column=9)
        ttk.Button(self, text='Kл', command=lambda: self.key_handler('kKKkлЛЛл')).grid(row=2, column=10)
        ttk.Button(self, text='Lд', command=lambda: self.key_handler('lLLlдДДд')).grid(row=2, column=11)
        ttk.Button(self, text='Ж:;', command=lambda: self.key_handler('::;;жЖЖж')).grid(row=2, column=12)
        ttk.Button(self, text='Э"\'', command=lambda: self.key_handler('""\'\'эЭЭэ')).grid(row=2, column=13)

        ttk.Button(self, textvariable=self.tkvars['shift'],
                   command=lambda: self.key_handler('shift')).grid(row=3, column=0, columnspan=3, sticky='we')
        ttk.Button(self, text='Zя', command=lambda: self.key_handler('zZZzяЯЯя')).grid(row=3, column=3)
        ttk.Button(self, text='Xч', command=lambda: self.key_handler('xXXxчЧЧч')).grid(row=3, column=4)
        ttk.Button(self, text='Сc', command=lambda: self.key_handler('cCCcсССс')).grid(row=3, column=5)
        ttk.Button(self, text='Vм', command=lambda: self.key_handler('vVVvмММм')).grid(row=3, column=6)
        ttk.Button(self, text='Bи', command=lambda: self.key_handler('bBBbиИИи')).grid(row=3, column=7)
        ttk.Button(self, text='Nт', command=lambda: self.key_handler('nNNnтТТт')).grid(row=3, column=8)
        ttk.Button(self, text='Mь', command=lambda: self.key_handler('mMMmьЬЬь')).grid(row=3, column=9)
        ttk.Button(self, text='Б<,', command=lambda: self.key_handler('<<,,бББб')).grid(row=3, column=10)
        ttk.Button(self, text='Ю>.', command=lambda: self.key_handler('>>..юЮЮю')).grid(row=3, column=11)
        ttk.Button(self, text='?/,.', command=lambda: self.key_handler('??//,,..')).grid(row=3, column=12, columnspan=2,
                                                                                         sticky='we')

        ttk.Button(self, text='Space', command=lambda: self.key_handler('space')).grid(row=4, column=4, columnspan=6,
                                                                                       sticky='we')

    def on_shift(self, state: bool):
        if state:
            self.shift = True
            self.tkvars['shift'].set('Shift (ON)')
        else:
            self.shift = False
            self.tkvars['shift'].set('Shift (OFF)')

    def on_capslock(self, state: bool):
        if state:
            self.capslock = True
            self.tkvars['capslock'].set('Caps Lock (ON)')
        else:
            self.capslock = False
            self.tkvars['capslock'].set('Caps Lock (OFF)')

    def smart_insert(self, symbols: str):
        """
        Parameters
        ------------
        symbols : str
            First symbol - shift: on, caps lock: on, language: EN
            Second symbol - shift: on, caps lock: off, language: EN
            Third symbol - shift: off, caps lock: on, language: EN
            Fourth symbol - shift: off, caps lock: off, language: EN
            Fifth symbol - shift: on, caps lock: on, language: RU
            Sixth symbol - shift: on, caps lock: off, language: RU
            Seventh symbol - shift: off, caps lock: on, language: RU
            Eighth symbol - shift: off, caps lock: off, language: RU
            Example - 'qQQqйЙЙй', '!!11!!11', '&&77??77', '{{[[хХХх'
        """
        entry = self.root.focused_entry
        lg = st.LANGUAGE
        if self.shift:
            self.on_shift(False)
            if lg == 'EN':
                entry.insert(tk.END, symbols[0] if self.capslock else symbols[1])
            elif lg == 'RU':
                entry.insert(tk.END, symbols[4] if self.capslock else symbols[5])
        else:
            if lg == 'EN':
                entry.insert(tk.END, symbols[2] if self.capslock else symbols[3])
            elif lg == 'RU':
                entry.insert(tk.END, symbols[6] if self.capslock else symbols[7])

    def key_handler(self, key):
        if key == 'shift':
            self.on_shift(not self.shift)
        elif key == 'capslock':
            self.on_capslock(not self.capslock)
        elif key == 'space':
            self.root.focused_entry.insert(tk.END, ' ')
        elif key == 'language':
            st.LANGUAGE = 'RU' if st.LANGUAGE == 'EN' else 'EN'
            self.root.root.tkvars['language'].set(st.LANGUAGE)
        elif key == 'backspace':
            obj = self.root.focused_entry
            obj.delete(len(obj.get())-1)
        elif key in st.KEY_BUFFER:
            self.smart_insert(key)

    def show_keyboard(self):
        self.grid(row=self.root.grid_size()[1], column=0, columnspan=self.root.grid_size()[0], sticky='we')
        keys = self.grid_slaves()
        keys[len(keys) // 2 - 5].focus_set()
        self.update()

    def hide_keyboard(self):
        self.grid_remove()
        self.root.focused_entry.focus_set()
