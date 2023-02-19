# Multi-frame tkinter application v2.3
import tkinter as tk
from tkinter import ttk


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        for c in range(3):
            self.columnconfigure(index=c, weight=1)
        for r in range(6):
            self.rowconfigure(index=r, weight=1)
        ttk.Label(self, text="This is the start page").grid()
        ttk.Button(self, text="Open page one",
                   command=lambda: master.switch_frame(PageOne)).grid()
        ttk.Button(self, text="Open page two",
                   command=lambda: master.switch_frame(PageTwo)).grid()


class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        ttk.Label(self, text="This is page one").grid()
        ttk.Button(self, text="Return to start page",
                   command=lambda: master.switch_frame(StartPage)).grid()


class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        ttk.Label(self, text="This is page two").grid()
        ttk.Button(self, text="Return to start page",
                   command=lambda: master.switch_frame(StartPage)).grid()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
