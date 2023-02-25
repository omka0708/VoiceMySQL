import sys
import time
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import pymysql
import json, pyaudio
from vosk import Model, KaldiRecognizer
from threading import Thread
from keyboard import Keyboard

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

        model_en, model_ru = Model('small_model_en_us'), Model('small_model_ru')
        rec_en, rec_ru = KaldiRecognizer(model_en, 16000), KaldiRecognizer(model_ru, 16000)
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        stream.start_stream()

        self.listening_thread = Thread(target=self.listen, args=(stream, rec_en, rec_ru))
        self.listening_thread.start()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

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
                if hasattr(self._frame, 'keyboard') and self._frame.keyboard.keyboard_isactive.get():
                    obj = self._frame.focused_entry
                else:
                    obj = self.focus_get()
                if obj.winfo_class() == 'TEntry':
                    obj.delete(0, tk.END)
            elif listened_text['RU'] == st.COMMANDS_MEANING['delete_word']:
                if hasattr(self._frame, 'keyboard') and self._frame.keyboard.keyboard_isactive.get():
                    obj = self._frame.focused_entry
                else:
                    obj = self.focus_get()
                if obj.winfo_class() == 'TEntry':
                    text = ' '.join(obj.get().split()[:-1])
                    obj.delete(0, tk.END)
                    obj.insert(0, text)
            elif hasattr(self._frame, 'keyboard') and listened_text['RU'] == st.COMMANDS_MEANING['keyboard_on']:
                self.commands['keyboard_on'] = False
                self.commands['keyboard_off'] = True
                self.commands['focus_left'] = True
                self.commands['focus_right'] = True
                self._frame.keyboard.keyboard_isactive.set(True)
            elif hasattr(self._frame, 'keyboard') and listened_text['RU'] == st.COMMANDS_MEANING['keyboard_off']:
                self.commands['keyboard_on'] = True
                self.commands['keyboard_off'] = False
                self.commands['focus_left'] = False
                self.commands['focus_right'] = False
                self._frame.keyboard.keyboard_isactive.set(False)

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
        if self._frame.keyboard.keyboard_isactive.get():
            container = self._frame.keyboard
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

        self.focused_entry = None
        self.keyboard = Keyboard(self)

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
        # self.root.switch_frame(ConnectionWindow)
        self.keyboard.keyboard_isactive.set(not self.keyboard.keyboard_isactive.get())

    def on_keyboard(self):
        if self.keyboard.keyboard_isactive.get():
            if self.focus_get().winfo_class() == 'TEntry':
                self.focused_entry = self.focus_get()
            else:
                self.focused_entry = self.winfo_children()[6]
            self.focused_entry.configure(takefocus=0)
            for widget in self.winfo_children():
                if widget.winfo_class() == 'TEntry' and widget is not self.focused_entry:
                    widget['state'] = 'disabled'

            self.keyboard.show_keyboard()

            self.root.geometry(f'{self.window_width}x'
                                      f'{self.window_height + self.keyboard.winfo_height()}+'
                                      f'{self.center_x}+{self.center_y}')

        else:
            for widget in self.winfo_children():
                if widget.winfo_class() == 'TEntry':
                    widget['state'] = 'enabled'
            self.keyboard.hide_keyboard()
            self.root.geometry(f'{self.window_width}x{self.window_height}+'
                          f'{self.center_x}+{self.center_y}')


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
