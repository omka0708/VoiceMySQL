import sys
import time
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import pymysql
import json, pyaudio
from vosk import Model, KaldiRecognizer
from threading import Thread

import settings as st


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.closing = False
        self.commands = {
            'focus_up': True, 'focus_down': True, 'focus_left': False, 'focus_right': False, 'change_lang': True,
            'invoke': True, 'delete_word': True, 'delete_entry': True, 'keyboard_on': True, 'keyboard_off': False
        }
        self.resizable(False, False)

        self.tkvars = {
            'listen': tk.StringVar(),
            'commands': tk.StringVar(value=self.get_command_words()),
            'language': tk.StringVar(value=st.LANGUAGE)}

        self.keyboard = tk.BooleanVar(value=False)
        self.keyboard_frame = None
        self.focused_entry = None
        self.caps_lock = False

        model_en, model_ru = Model('small_model_en_us'), Model('small_model_ru')
        rec_en, rec_ru = KaldiRecognizer(model_en, 16000), KaldiRecognizer(model_ru, 16000)
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        stream.start_stream()

        self.listening_thread = Thread(target=self.listen, args=(stream, rec_en, rec_ru))
        self.listening_thread.start()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.keyboard.trace_add('write', lambda *args: self.on_keyboard())

        self._frame = None
        self.switch_frame(ConnectMenu)

    def get_command_words(self):
        return '\n'.join(st.COMMANDS_MEANING[command] for command, boolean in self.commands.items() if boolean)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side="top", fill="both", expand=True)

    def listen(self, stream, rec_en, rec_ru):
        while True:
            if self.closing:
                sys.exit()
            data = stream.read(4000, exception_on_overflow=False)
            if (rec_en.AcceptWaveform(data) or rec_ru.AcceptWaveform(data)) and len(data) > 0:
                answer_en = json.loads(rec_en.Result())['text']
                answer_ru = json.loads(rec_ru.Result())['text']
                answer = {'EN': answer_en, 'RU': answer_ru}
                if answer:
                    self.tkvars['listen'].set(answer[st.LANGUAGE])
                    self.handler(answer)

    def handler(self, listened_text):
        if listened_text['RU'] in self.get_command_words():
            if listened_text['RU'] == st.COMMANDS_MEANING['focus_up']:
                self.change_focus(container=self._frame, focus='up')
            elif listened_text['RU'] == st.COMMANDS_MEANING['focus_down']:
                self.change_focus(container=self._frame, focus='down')
            elif listened_text['RU'] == st.COMMANDS_MEANING['focus_left']:
                self.change_focus(container=self._frame, focus='left')
            elif listened_text['RU'] == st.COMMANDS_MEANING['focus_right']:
                self.change_focus(container=self._frame, focus='right')
            elif listened_text['RU'] == st.COMMANDS_MEANING['change_lang']:
                st.LANGUAGE = 'RU' if st.LANGUAGE == 'EN' else 'EN'
            elif listened_text['RU'] == st.COMMANDS_MEANING['invoke']:
                obj = self.focus_get()
                if obj.winfo_class() == 'TButton':
                    obj.invoke()
            elif listened_text['RU'] == st.COMMANDS_MEANING['delete_entry']:
                obj = self.focus_get()
                if obj.winfo_class() == 'TEntry':
                    obj.delete(0, tk.END)
            elif listened_text['RU'] == st.COMMANDS_MEANING['delete_word']:
                obj = self.focus_get()
                if obj.winfo_class() == 'TEntry':
                    text = ' '.join(obj.get().split()[:-1])
                    obj.delete(0, tk.END)
                    obj.insert(0, text)
            elif listened_text['RU'] == st.COMMANDS_MEANING['keyboard_on']:
                self.commands['keyboard_on'] = False
                self.commands['keyboard_off'] = True
                self.commands['focus_left'] = True
                self.commands['focus_right'] = True
                self.keyboard.set(True)
            elif listened_text['RU'] == st.COMMANDS_MEANING['keyboard_off']:
                self.commands['keyboard_on'] = True
                self.commands['keyboard_off'] = False
                self.commands['focus_left'] = False
                self.commands['focus_right'] = False
                self.keyboard.set(False)

        # updating labels
        self.tkvars['commands'].set(self.get_command_words())
        self.tkvars['language'].set(st.LANGUAGE)

    def set_focus(self, container, row_ch: tuple, col_ch: tuple):
        max_columns, max_rows = container.grid_size()
        focusable_classes = ['TEntry', 'TButton']
        row = container.focus_get().grid_info()['row']
        column = container.focus_get().grid_info()['column']
        obj = container.grid_slaves(
            (row + row_ch[0] + max_rows) % max_rows,
            (column + col_ch[0] + max_columns) % max_columns)
        if obj and obj[0].winfo_class() in focusable_classes:
            obj[0].focus_set()
        else:
            obj = container.grid_slaves(
                (row + row_ch[1] + max_rows) % max_rows,
                (column + col_ch[1] + max_columns) % max_columns)
            if obj and obj[0].winfo_class() in focusable_classes:
                obj[0].focus_set()
            else:
                obj = container.grid_slaves(
                    (row + row_ch[2] + max_rows) % max_rows,
                    (column + col_ch[2] + max_columns) % max_columns)
                if obj and obj[0].winfo_class() in focusable_classes:
                    obj[0].focus_set()

    def change_focus(self, container, focus):
        if self.keyboard.get():
            container = self.keyboard_frame
        dy = container.focus_get().grid_info()['rowspan']
        dx = container.focus_get().grid_info()['columnspan']
        if focus == 'up':
            self.set_focus(container, (-dy, -dy, -dy), (0, dx, -dx))
        elif focus == 'down':
            self.set_focus(container, (dy, dy, dy), (0, dx, -dx))
        elif focus == 'left':
            self.set_focus(container, (0, dy, -dy), (-dx, -dx, -dx))
        elif focus == 'right':
            self.set_focus(container, (0, dy, -dy), (dx, dx, dx))

    def on_closing(self):
        self.closing = True
        sys.exit()

    def key_handler(self, key_text):
        print(key_text)

    def init_buttons(self):
        for column in range(13):
            self.keyboard_frame.columnconfigure(index=column, weight=1)
        for row in range(5):
            self.keyboard_frame.rowconfigure(index=row, weight=1)

        ttk.Button(self.keyboard_frame, text='~`Ё', command=lambda: self.key_handler('~`Ё')).grid(row=0, column=0)
        ttk.Button(self.keyboard_frame, text='!1', ).grid(row=0, column=1)
        ttk.Button(self.keyboard_frame, text='"@', ).grid(row=0, column=2)
        ttk.Button(self.keyboard_frame, text='№#', ).grid(row=0, column=3)
        ttk.Button(self.keyboard_frame, text=';$', ).grid(row=0, column=4)
        ttk.Button(self.keyboard_frame, text='%5', ).grid(row=0, column=5)
        ttk.Button(self.keyboard_frame, text=':^', ).grid(row=0, column=6)
        ttk.Button(self.keyboard_frame, text='?&', ).grid(row=0, column=7)
        ttk.Button(self.keyboard_frame, text='*8', ).grid(row=0, column=8)
        ttk.Button(self.keyboard_frame, text='(9', ).grid(row=0, column=9)
        ttk.Button(self.keyboard_frame, text=')0', ).grid(row=0, column=10)
        ttk.Button(self.keyboard_frame, text='_-', ).grid(row=0, column=11)
        ttk.Button(self.keyboard_frame, text='+=', ).grid(row=0, column=12)
        ttk.Button(self.keyboard_frame, text='Backspace', ).grid(row=0, column=13)

        ttk.Label(self.keyboard_frame, text='OFF', ).grid(row=1, column=0)

        ttk.Button(self.keyboard_frame, text='Qй', ).grid(row=1, column=1)
        ttk.Button(self.keyboard_frame, text='Wц', ).grid(row=1, column=2)
        ttk.Button(self.keyboard_frame, text='Eу', ).grid(row=1, column=3)
        ttk.Button(self.keyboard_frame, text='Rк', ).grid(row=1, column=4)
        ttk.Button(self.keyboard_frame, text='Tе', ).grid(row=1, column=5)
        ttk.Button(self.keyboard_frame, text='Yн', ).grid(row=1, column=6)
        ttk.Button(self.keyboard_frame, text='Uг', ).grid(row=1, column=7)
        ttk.Button(self.keyboard_frame, text='Iш', ).grid(row=1, column=8)
        ttk.Button(self.keyboard_frame, text='Oщ', ).grid(row=1, column=9)
        ttk.Button(self.keyboard_frame, text='Pз', ).grid(row=1, column=10)
        ttk.Button(self.keyboard_frame, text='{[х', ).grid(row=1, column=11)
        ttk.Button(self.keyboard_frame, text='}]ъ', ).grid(row=1, column=12)
        ttk.Button(self.keyboard_frame, text='|\\/', ).grid(row=1, column=13)

        ttk.Button(self.keyboard_frame, text='Caps Lock', ).grid(row=2, column=0, columnspan=2)
        ttk.Button(self.keyboard_frame, text='Aф', ).grid(row=2, column=2)
        ttk.Button(self.keyboard_frame, text='Sы', ).grid(row=2, column=3)
        ttk.Button(self.keyboard_frame, text='Dв', ).grid(row=2, column=4)
        ttk.Button(self.keyboard_frame, text='Fа', ).grid(row=2, column=5)
        ttk.Button(self.keyboard_frame, text='Gп', ).grid(row=2, column=6)
        ttk.Button(self.keyboard_frame, text='Hр', ).grid(row=2, column=7)
        ttk.Button(self.keyboard_frame, text='Jо', ).grid(row=2, column=8)
        ttk.Button(self.keyboard_frame, text='Kл', ).grid(row=2, column=9)
        ttk.Button(self.keyboard_frame, text='Lд', ).grid(row=2, column=10)
        ttk.Button(self.keyboard_frame, text='Ж:;', ).grid(row=2, column=11)
        ttk.Button(self.keyboard_frame, text='Э"\'', ).grid(row=2, column=12)

        ttk.Button(self.keyboard_frame, text='Shift', ).grid(row=3, column=0, columnspan=2)
        ttk.Button(self.keyboard_frame, text='Zя', ).grid(row=3, column=2)
        ttk.Button(self.keyboard_frame, text='Xч', ).grid(row=3, column=3)
        ttk.Button(self.keyboard_frame, text='Сc', ).grid(row=3, column=4)
        ttk.Button(self.keyboard_frame, text='Vм', ).grid(row=3, column=5)
        ttk.Button(self.keyboard_frame, text='Bи', ).grid(row=3, column=6)
        ttk.Button(self.keyboard_frame, text='Nт', ).grid(row=3, column=7)
        ttk.Button(self.keyboard_frame, text='Mь', ).grid(row=3, column=8)
        ttk.Button(self.keyboard_frame, text='Б<,', ).grid(row=3, column=9)
        ttk.Button(self.keyboard_frame, text='Ю>.', ).grid(row=3, column=10)
        ttk.Button(self.keyboard_frame, text='?/', ).grid(row=3, column=11)
        ttk.Button(self.keyboard_frame, text=',.', ).grid(row=3, column=12)

        ttk.Button(self.keyboard_frame, text='Space', ).grid(row=4, column=4, columnspan=6, sticky='we')

    def on_keyboard(self):
        if self.keyboard.get():
            self._frame.focused_entry = self._frame.focus_get()
            self._frame.focused_entry.configure(takefocus=0)
            for widget in self._frame.winfo_children():
                if widget.winfo_class() == 'TEntry' and widget is not self._frame.focused_entry:
                    widget['state'] = 'disabled'
            self.keyboard_frame = ttk.Frame(self._frame, borderwidth=1, relief='groove', )
            self.keyboard_frame.grid(row=self._frame.grid_size()[1], column=0,
                                     columnspan=self._frame.grid_size()[0], sticky='we')

            self.init_buttons()

            self.keyboard_frame.update()
            self._frame.root.geometry(f'{self._frame.window_width}x'
                                      f'{self._frame.window_height + self.keyboard_frame.winfo_height()}+'
                                      f'{self._frame.center_x}+{self._frame.center_y}')

            self.keyboard_frame.grid_slaves()[-1].focus_set()

        else:
            for widget in self._frame.winfo_children():
                if widget.winfo_class() == 'TEntry':
                    widget['state'] = 'enabled'
            self.keyboard_frame.grid_remove()
            self.geometry(f'{self._frame.window_width}x{self._frame.window_height}+'
                          f'{self._frame.center_x}+{self._frame.center_y}')
            self._frame.focused_entry.focus_set()


class ConnectMenu(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        root.title("VoiceMySQL")

        self.window_width = 500
        self.window_height = 250
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        self.center_x = int(self.screen_width / 2 - self.window_width / 2)
        self.center_y = int(self.screen_height / 2 - self.window_height / 2 - 50)

        root.geometry(f'{self.window_width}x{self.window_height}+{self.center_x}+{self.center_y}')

        for c in range(3):
            self.columnconfigure(index=c, weight=1)
        for r in range(6):
            self.rowconfigure(index=r, weight=1)

        self.img = ImageTk.PhotoImage(Image.open("micro.png"))

        label_mic = ttk.Label(self, image=self.img)
        label_mic.grid(row=0, column=0)

        label_listening = ttk.Label(self, textvariable=root.tkvars['listen'], borderwidth=2, relief='groove', padding=5,
                                    width=20, anchor=tk.CENTER, background='white')
        label_listening.grid(row=0, column=1)

        label_txt_commands = ttk.Label(self, text='commands:')
        label_txt_commands.grid(row=0, column=2)

        label_commands = ttk.Label(self, textvariable=root.tkvars['commands'], borderwidth=2, relief='groove',
                                   padding=5,
                                   width=20, background='white', foreground='red',
                                   justify=tk.CENTER, anchor=tk.CENTER)

        label_commands.grid(row=1, column=2, rowspan=4, sticky='ns', padx=10)

        label_host = ttk.Label(self, text='host:')
        label_host.grid(row=1, column=0)
        entry_host = ttk.Entry(self)
        entry_host.grid(row=1, column=1)
        entry_host.focus_set()

        label_user = ttk.Label(self, text='user:')
        label_user.grid(row=2, column=0)
        entry_user = ttk.Entry(self)
        entry_user.grid(row=2, column=1)

        label_port = ttk.Label(self, text='port:')
        label_port.grid(row=3, column=0)
        entry_port = ttk.Entry(self)
        entry_port.grid(row=3, column=1)

        label_password = ttk.Label(self, text='password:')
        label_password.grid(row=4, column=0, ipadx=10)
        entry_password = ttk.Entry(self)
        entry_password.grid(row=4, column=1)

        button_connect = ttk.Button(self, text='Connect', command=self.connect)
        button_connect.grid(row=5, column=0, columnspan=2)

        label_listening_lang = ttk.Label(self, textvariable=root.tkvars['language'], text=st.LANGUAGE)
        label_listening_lang.grid(row=5, column=2)

        root.bind("<Return>", lambda e: self.connect())
        root.bind("<Up>", lambda e: root.change_focus(self, 'up'))
        root.bind("<Down>", lambda e: root.change_focus(self, 'down'))
        root.bind("<Left>", lambda e: root.change_focus(self, 'left'))
        root.bind("<Right>", lambda e: root.change_focus(self, 'right'))

    def connect(self):
        self.root.switch_frame(ConnectionWindow)


class ConnectionWindow(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root

        root.title("VoiceMySQL")
        root.resizable(False, False)

        window_width = 250
        window_height = 250
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2 - 50)

        root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


if __name__ == "__main__":
    app = App()
    app.mainloop()
