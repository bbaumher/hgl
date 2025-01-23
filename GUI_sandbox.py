import os
import re
import time

from synap import ProcessSynapData
from synap import TestType

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
    
def isCSV(path):
        print(path)
        print(re.search(path, ".+\\.csv"))
        return bool(re.search(path, ".+\\.csv"))
    


class Upload(ttk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.file_var = tk.StringVar()
        txt_box = tk.Entry(self,
                        textvariable = self.file_var)
        txt_box.grid(column = 2, row = 1, padx = 10, pady = 10)
        btn = tk.Button(self,
                        text = 'Browse',
                        command=self.getFilePath)
        btn.grid(column = 1, row = 1, padx = 10, pady = 10)

    def getFilePath(self):
        file_path = filedialog.askopenfilename(initialdir = "/",
                                           title = "Select a .csv file",
                                           filetypes=(("CSV Files","*.csv"),))
        self.file_var.set(file_path)



        
class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.input_path = None
        self.input_search_dir = '/Users/bex/hgl'

        self.title('Synap Upload')  

        # Layout            
        width = 640
        height = 480
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.resizable(0, 0)

        # Create the frames for each section
       
        
        # Create input widgets
        input_button = tk.Button(self, text='Browse for input CSV', command=self.select_input)
        self.input_text = tk.StringVar()
        input_entry = tk.Entry(textvariable=self.input_text, width=30)

        # Place input widgets on screen
        input_button.grid(column=1, row=1, padx=10, pady=10)
        input_entry.grid(column=2, row=1, padx=10, pady=10)

        # Create Option 
        option_label = tk.Label(text='Choose Test Template:')
        # datatype of menu text 
        self.clicked = tk.StringVar() 

        # initial menu text 
        self.clicked.set(TestType.SAT_Init.value ) 

        # Create Dropdown menu 
        drop = tk.OptionMenu( self , self.clicked , *[option.value for option in TestType]) 
        drop.grid(column=2, row=3, padx=10, pady=10)
        option_label.grid(column=1, row=3, padx=10, pady=10)
                


        # Create output widgets
        output_label = tk.Label(text='Save As')
        self.output_text = tk.StringVar()
        self.output_text.set('SAT Initial Diagnostic <student>')
        output_entry = tk.Entry(textvariable=self.output_text, width=30)

        # Place output widgets on screen
        output_label.grid(column=1, row=2, padx=10, pady=10)
        output_entry.grid(column=2, row=2, padx=10, pady=10)

        # Create label with URL
        self.label_var = tk.StringVar()
        self.label_var.set("")
        url_label = tk.Label(textvariable=self.label_var, width=30)

        url_label.grid(column=2, row=4, padx=10, pady=10)
  
        # Create copy button
        self.copy_btn = tk.Button(self, text='Copy to Clipboard', command=lambda: self.gtc(self.label_var.get()))
        
        

        # Create lifecycle widgets
        run_btn = tk.Button(self, text='Run!', command=self.process_input)
        #run_btn.pack(side=tk.LEFT, padx=5, pady=5)
        quit_btn = tk.Button(self, text='Quit', command=self.quit)
        #quit_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        # Place lifecycle widgets on screen
        run_btn.grid(column=1, row=4, padx=10, pady=10)
        quit_btn.grid(column=1, row=5, padx=10, pady=10)

        # pack 
        #output_label.pack()
        #output_entry.pack()
        #input_entry.pack()

    def gtc(self, dtxt):
        self.clipboard_clear()
        self.clipboard_append(dtxt)

    def dudso_test(self):
        time.sleep(2)
        return "https://docs.google.com/spreadsheets/d/1UJFHBPPUDTQFRZ-EjXFv19I2uYfcE40JxQptYwmItjY/edit?gid=902962355#gid=902962355"
    
    
    def process_input(self):
        print("Source CSV: ", self.input_path)
        print("Output title: ", self.output_text.get())
        self.label_var.set("...running")     
        url = ProcessSynapData(self.input_path, self.output_text.get(), TestType(self.clicked.get()))
        self.label_var.set(url)
        self.copy_btn.grid(column=3, row=4, padx=10, pady=10)


    def select_input(self):
        self.input_path = filedialog.askopenfilename(
            initialdir = self.input_search_dir,
            title = "Select a .csv file",
            filetypes=(("CSV Files","*.csv"),)
        )
        self.input_text.set(self.input_path)  



if __name__ == "__main__":

    app = App()
    app.mainloop()
