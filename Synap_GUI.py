import tkinter as tk
from tkinter import filedialog

class NewWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('New Window')
        self.file_var = tk.StringVar()
        txt_box = tk.Entry(self,
                        textvariable = self.file_var.get())
        txt_box.grid(column = 2, row = 1, padx = 10, pady = 10)
        btn = tk.Button(self,
                        text = 'Browse',
                        command=self.getFilePath)
        btn.grid(column = 1, row = 1, padx = 10, pady = 10)

    def getFilePath(self):
        file_path = filedialog.askopenfilename(initialdir = "/",
                                           title = "Select a file")
        self.file_var.set(file_path)
        
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Main Window')
        btn = tk.Button(self,
                        text='New Window',
                        height = 3,
                        width = 12,
                        command=self.open_new_window)
        btn.grid(column = 1, row = 1, padx = 10, pady= 10)
        
    def open_new_window(self):
        window = NewWindow(self)
        window.grab_set()


if __name__ == "__main__":
    app = App()
    app.mainloop()