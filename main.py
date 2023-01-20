#%%
#!/usr/bin/env python3
"""
MIT License

Copyright (c) 2023 Okyaz Eminaga

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from collections import defaultdict
from sys import exec_prefix
import tkinter as tk
from tkinter import ttk
from tkinter import *
from turtle import width  
from PIL import ImageTk,Image  
import matplotlib.pyplot as plt
from tkinter.messagebox import showinfo

import os
import subprocess
import datetime
import pandas as pd
from tkinter.messagebox import showinfo
#%%
os.chdir(os.path.dirname(__file__))
#%%
class InputWindow(object):
    def __init__(self) -> None:
        pass
    def AddNewCase(self):
        os.system("python3 CaseEntry.py")
    def ViewAndEditCase(self):
        os.system("python3 LabelingManager.py --source ../Data --script LabelTheImages.py --prefix Images")
    def GenerateReports(self):
        fns = ["python3 Calculate.py", "python3 Summarize.py", "python3 CheckFiles.py"]
        length=len(fns)
        for i, fn in enumerate(fns):
            os.system(fn)
            self.pb1['value'] = round(100/(length-(i)))
            self.root.update_idletasks()
        self.pb1['value'] = 100
        self.root.update_idletasks()
        
        showinfo("Finished", "Report generation is completed.")
        self.pb1['value'] = 0
    def ExportCases(self):
        os.system("python3 DataSharing.py")
    def create_main_window(self):
        flx=__file__.split(os.sep)[-3]
        self.root =tk.Tk()
        self.root.title(f'Main menu ({flx})')
        #self.root.geometry('512x512')
        self.btn_AddNewCase = tk.Button(self.root, text="New case", command=self.AddNewCase)
        self.btn_AddNewCase.pack(fill=tk.X)
        self.btn_ViewAndEditCase = tk.Button(self.root, text="View or label the contents in each case", command=self.ViewAndEditCase)
        self.btn_ViewAndEditCase.pack(fill=tk.X)
        self.btn_GenerateReports = tk.Button(self.root, text="Generate summary and validation reports", command=self.GenerateReports)
        self.btn_GenerateReports.pack(fill=tk.X)
        self.btn_ExportCases = tk.Button(self.root, text="Export cases", command=self.ExportCases)
        self.btn_ExportCases.pack(fill=tk.X)
        self.pb1 = ttk.Progressbar(self.root, orient=HORIZONTAL, length=100)
        self.pb1.pack(fill=tk.X)
        self.root.mainloop()
    def Show(self):
        self.create_main_window()
if __name__ == "__main__":
    win=InputWindow()
    win.Show()